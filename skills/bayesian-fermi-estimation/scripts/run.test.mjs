import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import test from 'node:test';

const runner = fileURLToPath(new URL('./run.mjs', import.meta.url));
function call(source, args = []) {
  return spawnSync(process.execPath, [runner, ...args], { input: source, encoding: 'utf8' });
}
test('summarize a seeded distribution and export aligned draws', () => {
  const code='x = normal(0,1)\n{x:x, double:x*2, observations:[1,2]}';
  const result=call(code, ['--samples', '100', '--seed', 'test', '--draws']);
  assert.equal(result.status, 0, result.stderr);
  const {value,seed}=JSON.parse(result.stdout);
  assert.equal(seed,'test'); assert.deepEqual(value.observations,[1,2]);
  assert.equal(value.x.draws.length,100);
  assert.deepEqual(value.double.draws,value.x.draws.map(n=>2*n));
  assert.deepEqual(call(code, ['--samples','100','--seed','test','--draws']).stdout,result.stdout);
});
test('return a structured error on an invalid program or sample count', () => {
  for(const [code,args] of [['sqrt(',[]],['1',['--samples','0']]]) {
    const result=call(code,args); assert.equal(result.status,2);assert(JSON.parse(result.stderr).error);
  }
});
