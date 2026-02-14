import http from 'k6/http';
import { check } from 'k6';

export const options = {
  scenarios: {
    steady: {
      executor: 'constant-arrival-rate',
      rate: parseInt(__ENV.RATE || '1', 10),
      timeUnit: '1s',
      duration: __ENV.DURATION || '30s',
      preAllocatedVUs: parseInt(__ENV.PRE_VUS || '200', 10),
      maxVUs: parseInt(__ENV.MAX_VUS || '500', 10),
    },
  },
};

const BASE_URL = __ENV.BASE_URL;
const WORKLOAD = __ENV.WORKLOAD || 'llm'; // cpu | llm | upload | pubsub
const CPU_SECONDS = parseInt(__ENV.CPU_SECONDS || '5', 10);

function payloadLLM() {
  return JSON.stringify({ prompt: 'a'.repeat(1000) });
}
function payloadPubSub() {
  return JSON.stringify({ msg: 'b'.repeat(1024) });
}
function payloadCPU() {
  return JSON.stringify({ seconds: CPU_SECONDS });
}
function payloadUpload1MB() {
  const size = 1024 * 1024;
  const bytes = new Uint8Array(size);
  for (let i = 0; i < size; i++) bytes[i] = i % 256;
  return bytes;
}

export default function () {
  let res;

  if (WORKLOAD === 'cpu') {
    res = http.post(`${BASE_URL}/cpu`, payloadCPU(), {
      headers: { 'Content-Type': 'application/json' },
      timeout: '120s',
    });
    check(res, { 'cpu 200': (r) => r.status === 200 });
    return;
  }

  if (WORKLOAD === 'llm') {
    res = http.post(`${BASE_URL}/llm`, payloadLLM(), {
      headers: { 'Content-Type': 'application/json' },
    });
    check(res, { 'llm 200': (r) => r.status === 200 });
    return;
  }

  if (WORKLOAD === 'pubsub') {
    res = http.post(`${BASE_URL}/pubsub`, payloadPubSub(), {
      headers: { 'Content-Type': 'application/json' },
    });
    check(res, { 'pubsub 200': (r) => r.status === 200 });
    return;
  }

  if (WORKLOAD === 'upload') {
    const bytes = payloadUpload1MB();
    res = http.post(`${BASE_URL}/upload`, bytes, {
      headers: { 'Content-Type': 'application/octet-stream' },
      timeout: '120s',
    });
    check(res, { 'upload 200': (r) => r.status === 200 });
    return;
  }

  throw new Error(`Unknown WORKLOAD=${WORKLOAD}`);
}
