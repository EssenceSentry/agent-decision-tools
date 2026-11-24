import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import {
  mkdtempSync,
  mkdirSync,
  readFileSync,
  readdirSync,
  writeFileSync,
  rmSync,
  utimesSync,
} from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

const python = process.env.PYTHON || "python3";
const root = fileURLToPath(new URL("..", import.meta.url));
const skill = path.join(root, "skills/record-for-resumption");
function fixture(t) {
  const dir = mkdtempSync(path.join(tmpdir(), "merged skills "));
  t.after(() => rmSync(dir, { recursive: true, force: true }));
  return dir;
}
function run(bin, args, options = {}) {
  const result = spawnSync(bin, args, { encoding: "utf8", ...options });
  assert.equal(result.status, 0, result.stderr);
  return result.stdout;
}

test("map relative re-exports to the owning definition without importing code", (t) => {
  const dir = fixture(t),
    lib = path.join(dir, "metrics"),
    consumer = path.join(dir, "client");
  mkdirSync(lib);
  mkdirSync(consumer);
  writeFileSync(
    path.join(lib, "__init__.py"),
    "from .core import score as rate\n",
  );
  writeFileSync(
    path.join(lib, "core.py"),
    'raise RuntimeError("never import this")\ndef score(x): return x\n',
  );
  writeFileSync(
    path.join(consumer, "caller.py"),
    "from metrics import rate as measure\nmeasure(5)\nimport metrics as m\nm.rate(7)\n",
  );
  writeFileSync(path.join(consumer, "broken.py"), "def invalid(:");
  const output = JSON.parse(
    run("python3", [
      path.join(root, "skills/gather-what-is-known/scripts/usage_map.py"),
      "--library",
      lib,
      "--consumer",
      consumer,
    ]),
  );
  assert(
    output.internal_imports.some((i) => i.requested === "metrics.core.score"),
  );
  assert(
    output.consumer_imports.some(
      (i) => i.requested === "metrics.rate" && i.owner === "metrics.core.score",
    ),
  );
  assert(
    output.calls.filter((i) => i.owner === "metrics.core.score").length === 2,
  );
  assert(output.gaps.some((i) => i.file.endsWith("broken.py")));
});

for (const host of ["claude", "codex"])
  test(
    host +
      " registered checkpoint preserves fresh progress, respects scope and survives repeated events",
    (t) => {
      const dir = fixture(t),
        state = path.join(dir, "state"),
        project = path.join(dir, "work tree");
      mkdirSync(project);
      mkdirSync(path.join(project, "." + host));
      const config = path.join(
        project,
        ...(host === "claude"
          ? [".claude", "settings.local.json"]
          : [".codex", "hooks.json"]),
      );
      const outside = { type: "command", command: "echo unrelated" };
      writeFileSync(
        config,
        JSON.stringify({ hooks: { Stop: [{ hooks: [outside] }] } }),
      );
      const args = [
        path.join(skill, "scripts/register_hook.py"),
        host,
        project,
        "--record",
        "research.md",
        "--state-dir",
        state,
      ];
      run(python, args);
      run(python, args);
      const hooks = JSON.parse(readFileSync(config)).hooks;
      assert.deepEqual(hooks.Stop, [{ hooks: [outside] }]);
      assert.equal(hooks.PreCompact.length, 1);
      const registration = hooks.PreCompact[0];
      assert(new RegExp(registration.matcher).test("manual"));
      assert(new RegExp(registration.matcher).test("auto"));
      const cmd = registration.hooks[0].command,
        transcript = path.join(dir, "log.jsonl");
      const envelope = (text) =>
        host === "claude"
          ? {
              type: "assistant",
              message: { role: "assistant", content: [{ type: "text", text }] },
            }
          : {
              type: "response_item",
              payload: {
                type: "message",
                role: "assistant",
                content: [{ type: "output_text", text }],
              },
            };
      writeFileSync(
        transcript,
        [
          JSON.stringify(
            envelope(
              "Tried a monthly fit. Dropped it after the placebo failed.",
            ),
          ),
          JSON.stringify({
            type: "tool_result",
            content: "EXCLUDED-TOOL-TEXT",
          }),
          JSON.stringify(envelope("Next check is a held-out week.")),
        ].join("\n"),
      );
      writeFileSync(
        path.join(project, "research.md"),
        "Assumption: stable cohort.\n",
      );
      const event = {
        hook_event_name: "PreCompact",
        trigger: "auto",
        cwd: project,
        session_id: "../../unsafe-id",
        transcript_path: transcript,
      };
      const dispatch = (e) =>
        run("/bin/sh", ["-c", cmd], { cwd: project, input: JSON.stringify(e) });
      dispatch(event);
      dispatch({ ...event, trigger: "manual" });
      let files = readdirSync(state, { recursive: true }).filter((n) =>
        n.endsWith(".md"),
      );
      assert.equal(files.length, 1);
      const result = readFileSync(path.join(state, files[0]), "utf8");
      for (const part of ["placebo failed", "held-out week", "stable cohort"])
        assert(result.includes(part));
      assert(!result.includes("EXCLUDED-TOOL-TEXT"));
      const readArgs = [
        path.join(skill, "scripts/read_checkpoint.py"),
        host,
        project,
        "--state-dir",
        state,
      ];
      assert.equal(run(python, readArgs), result);
      dispatch({ ...event, cwd: dir, session_id: "other" });
      dispatch({ ...event, hook_event_name: "Stop", session_id: "other" });
      assert.deepEqual(
        readdirSync(state, { recursive: true }).filter((n) =>
          n.endsWith(".md"),
        ),
        files,
      );
      dispatch({
        ...event,
        session_id: "another session",
        transcript_path: null,
      });
      assert.equal(
        readdirSync(state, { recursive: true }).filter((n) => n.endsWith(".md"))
          .length,
        2,
      );
      const keys = run(python, readArgs).trim().split("\n").slice(1);
      assert.equal(keys.length, 2);
      assert(
        keys.some(
          (k) =>
            run(python, [...readArgs, "--session-key", k]) === result,
        ),
      );
      rmSync(path.join(project, "research.md"));
      writeFileSync(
        transcript,
        JSON.stringify(
          envelope(
            "```handoff-state\nNext: recheck cohort A at revision 25.\n```",
          ),
        ),
      );
      dispatch(event);
      const updated = keys.map((k) =>
        run(python, [...readArgs, "--session-key", k]),
      );
      assert(
        updated.some((s) =>
          s.includes("## Latest explicit handoff\n\nNext: recheck cohort A"),
        ),
      );
      dispatch({ ...event, transcript_path: null });
      assert.deepEqual(
        keys.map((k) =>
          run(python, [...readArgs, "--session-key", k]),
        ),
        updated,
      );
    },
  );

test("checkpoint is a bounded recovery copy that can be cleared", (t) => {
  const dir = fixture(t),
    state = path.join(dir, "state"),
    project = path.join(dir, "work tree"),
    transcript = path.join(dir, "log.jsonl"),
    registrar = path.join(skill, "scripts/register_hook.py");
  mkdirSync(project);
  const command = (...extra) =>
    JSON.parse(
      run(python, [
        registrar,
        "claude",
        project,
        "--state-dir",
        state,
        "--print",
        ...extra,
      ]),
    ).hooks.PreCompact[0].hooks[0].command;
  const say = (text) =>
    JSON.stringify({
      type: "assistant",
      message: { role: "assistant", content: [{ type: "text", text }] },
    });
  const event = {
    hook_event_name: "PreCompact",
    trigger: "auto",
    cwd: project,
    session_id: "current",
    transcript_path: transcript,
  };
  const dispatch = (cmd, e = event) =>
    run("/bin/sh", ["-c", cmd], { cwd: project, input: JSON.stringify(e) });
  const snapshots = () =>
    readdirSync(state, { recursive: true }).filter((n) => n.endsWith(".md"));
  const readArgs = [
    path.join(skill, "scripts/read_checkpoint.py"),
    "claude",
    project,
    "--state-dir",
    state,
  ];

  writeFileSync(
    transcript,
    ["one", "two", "three", "four", "five"]
      .map((n) => say("note " + n))
      .join("\n"),
  );
  dispatch(command());
  let saved = run(python, readArgs);
  assert(!saved.includes("note two"));
  for (const part of ["note three", "note four", "note five"])
    assert(saved.includes(part));

  writeFileSync(
    transcript,
    [
      say("chatter"),
      say("```handoff-state\nNext: rerun cohort B.\n```"),
    ].join("\n"),
  );
  dispatch(command("--progress", "0"));
  saved = run(python, readArgs);
  assert(saved.includes("## Latest explicit handoff\n\nNext: rerun cohort B."));
  assert(!saved.includes("chatter"));
  assert(!saved.includes("Recent progress"));

  for (const round of [1, 2, 3, 4]) {
    writeFileSync(transcript, say("round " + round));
    dispatch(command("--keep", "2"));
  }
  assert.equal(snapshots().length, 2);
  assert(run(python, readArgs).includes("round 4"));

  dispatch(command(), { ...event, session_id: "abandoned" });
  assert.equal(snapshots().length, 3);
  const projectDir = path.join(state, readdirSync(state)[0]);
  const [abandoned] = readdirSync(projectDir, { withFileTypes: true })
    .filter((item) => item.isDirectory()).map((item) => item.name)
    .map((session) => path.join(projectDir, session))
    .filter((folder) => readdirSync(folder).length === 2);
  const longAgo = new Date(Date.now() - 40 * 86400000);
  for (const name of readdirSync(abandoned))
    utimesSync(path.join(abandoned, name), longAgo, longAgo);
  writeFileSync(transcript, say("round 5"));
  dispatch(command("--keep", "2", "--max-age-days", "30"));
  assert.equal(readdirSync(projectDir, {withFileTypes:true}).filter((item) => item.isDirectory()).length, 1);
  assert.equal(snapshots().length, 2);
  assert(run(python, readArgs).includes("round 5"));

  assert.match(run(python, [...readArgs, "--clear"]), /Cleared/);
  assert.equal(snapshots().length, 0);
  assert.equal(spawnSync(python, readArgs).status, 1);

  for (const bad of [
    ["--progress", "9"],
    ["--keep", "0"],
    ["--max-age-days", "soon"],
  ])
    assert.equal(
      spawnSync(python, [
        registrar,
        "claude",
        project,
        "--print",
        ...bad,
      ]).status,
      1,
    );
});

test("pollution locator distinguishes clean, identified, and invalid trials", (t) => {
  const dir = fixture(t),
    module = path.join(
      root,
      "skills/reproduce-a-defect/scripts/find_polluter.py",
    );
  const runCase = (...names) =>
    spawnSync(
      python,
      [
        module,
        "--watch",
        "trace.txt",
        "--runner",
        process.execPath,
        "--",
        ...names,
      ],
      { cwd: dir, encoding: "utf8" },
    );
  writeFileSync(path.join(dir, "good case.cjs"), "");
  writeFileSync(
    path.join(dir, "bad.cjs"),
    "require('node:fs').writeFileSync('trace.txt','1')",
  );
  writeFileSync(path.join(dir, "invalid.cjs"), "process.exit(5)");
  assert.equal(runCase("good case.cjs").status, 0);
  assert.equal(runCase("invalid.cjs").status, 2);
  const found = runCase("good case.cjs", "bad.cjs");
  assert.equal(found.status, 1);
  assert.equal(JSON.parse(found.stdout).test, "bad.cjs");
  assert.equal(runCase("good case.cjs").status, 2);
});

test("debt scan includes untracked source comments and respects git ignores", (t) => {
  const dir = fixture(t);
  run("git", ["init", "-q"], { cwd: dir });
  writeFileSync(path.join(dir, ".gitignore"), "cache/\n");
  mkdirSync(path.join(dir, "cache"));
  writeFileSync(path.join(dir, "cache", "bad.py"), "# shortcut: ignored\n");
  writeFileSync(
    path.join(dir, "local.py"),
    "# ponytail: single worker until demand exceeds eight\n",
  );
  const script = path.join(skill, "scripts/scan_debt.py");
  const output = run(python, [script], { cwd: dir });
  assert(output.includes("local.py:1"));
  assert(!output.includes("ignored"));
});

test("a new project can bootstrap an ADR and its index without overwriting a decision", (t) => {
  const dir = fixture(t),
    script = path.join(
      root,
      "skills/record-a-decision/scripts/new_adr.py",
    );
  const args = [
    script,
    "--repo-root",
    dir,
    "--dir",
    "decisions",
    "--title",
    "Keep stable IDs",
    "--update-index",
    "--json",
  ];
  const result = JSON.parse(run(python, args));
  assert(
    readFileSync(result.indexPath, "utf8").includes(
      path.basename(result.createdAdrPath),
    ),
  );
  const before = readFileSync(result.createdAdrPath, "utf8");
  assert(spawnSync(python, args).status !== 0);
  assert.equal(readFileSync(result.createdAdrPath, "utf8"), before);
});

test("SQL probes catch per-key errors even when a global total looks right", () => {
  const guide = readFileSync(
    path.join(
      root,
      "skills/design-an-evidence-check/references/sql-probes.md",
    ),
    "utf8",
  );
  const queries = [...guide.matchAll(/^```sql\n([\s\S]*?)^```/gm)].map(
    (match) => match[1],
  );
  const raw = run(
    "python3",
    [
      "-c",
      [
        "import sqlite3, json, sys",
        'db=sqlite3.connect(":memory:")',
        'db.executescript("CREATE TABLE orders(id,amount_cents,deleted_at); CREATE TABLE events(order_id); INSERT INTO orders VALUES(1,90,NULL),(2,-90,NULL),(3,0,1); INSERT INTO events VALUES(1),(1),(2),(2),(3),(4);")',
        "print(json.dumps([db.execute(q).fetchall() for q in json.load(sys.stdin)]))",
      ].join("\n"),
    ],
    { input: JSON.stringify(queries) },
  );
  assert.deepEqual(JSON.parse(raw), [
    [
      [1, 2, 180, 90],
      [2, 2, -180, -90],
    ],
    [],
    [
      [3, 1],
      [4, 1],
    ],
  ]);
});
