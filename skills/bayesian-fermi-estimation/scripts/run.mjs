import { readFileSync } from 'node:fs';
import { parseArgs } from 'node:util';
import { run } from '@quri/squiggle-lang';

function quantile(distribution, environment, probability) {
  const result = distribution.inv(environment, probability);
  if (!result.ok) throw new Error(String(result.value));
  return result.value;
}

function summarize(distribution, environment, includeDraws) {
  const summary = {
    mean: distribution.mean(environment),
    p10: quantile(distribution, environment, 0.1),
    median: quantile(distribution, environment, 0.5),
    p90: quantile(distribution, environment, 0.9),
  };
  if (includeDraws) {
    if (distribution.tag !== 'SampleSet') {
      throw new Error('Use SampleSet.fromDist on symbolic inputs before combining them to export aligned draws.');
    }
    summary.draws = distribution.getSamples();
  }
  return summary;
}

function exportValue(item, environment, includeDraws) {
  const convert = (child) => exportValue(child, environment, includeDraws);
  switch (item.tag) {
    case 'Dist':
      return summarize(item.value, environment, includeDraws);
    case 'Array':
      return item.value.getValues().map(convert);
    case 'Dict':
      return Object.fromEntries(item.value.entries().map(([key, value]) => [key, convert(value)]));
    case 'Number':
    case 'Bool':
    case 'String':
      return item.asJS();
    default:
      throw new Error(`Return a number, distribution, list or record. Received ${item.tag}.`);
  }
}

async function main() {
  const { values, positionals } = parseArgs({
    allowPositionals: true,
    options: {
      seed: { type: 'string', default: '42' },
      samples: { type: 'string', default: '1000' },
      draws: { type: 'boolean', default: false },
      help: { type: 'boolean', default: false },
    },
  });
  if (values.help) {
    console.log('node run.mjs [--samples N] [--seed TEXT] [--draws] [program.squiggle]\nOmit the filename to read Squiggle from stdin. Outputs JSON.');
    return;
  }
  if (positionals.length > 1) throw new Error('Supply at most one Squiggle file.');
  const count = Number(values.samples);
  if (!Number.isSafeInteger(count) || count < 6) {
    throw new Error('Squiggle sample sets require at least six samples.');
  }
  const environment = { sampleCount: count, xyPointLength: 1000, seed: values.seed };
  const source = readFileSync(positionals[0] ?? 0, 'utf8');
  const execution = await run(source, { environment });
  if (!execution.result.ok) throw new Error(String(execution.result.value));
  const value = exportValue(execution.result.value.result, environment, values.draws);
  const output = { seed: values.seed, requested_samples: count, value };
  console.log(JSON.stringify(output, (_key, numberOrValue) => {
    if (typeof numberOrValue === 'number' && !Number.isFinite(numberOrValue)) {
      throw new Error('The calculation returned a non-finite value. Check the inputs and support.');
    }
    return numberOrValue;
  }));
}

try {
  await main();
} catch (error) {
  console.error(JSON.stringify({ error: String(error.message ?? error) }));
  process.exitCode = 2;
}
