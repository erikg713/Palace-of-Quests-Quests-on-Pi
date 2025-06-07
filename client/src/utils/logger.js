// logger.js

import fs from 'fs';
import path from 'path';

const LOG_LEVELS = ['DEBUG', 'INFO', 'WARN', 'ERROR'];
const DEFAULT_LEVEL = 'INFO';
const LOG_DIR = process.env.LOG_DIR || path.resolve(process.cwd(), 'logs');
const LOG_FILE = process.env.LOG_FILE || 'application.log';
const LOG_PATH = path.join(LOG_DIR, LOG_FILE);

const envLevel = (process.env.LOG_LEVEL || DEFAULT_LEVEL).toUpperCase();
const minLevelIdx = LOG_LEVELS.indexOf(envLevel);

function ensureLogDir() {
  if (!fs.existsSync(LOG_DIR)) {
    fs.mkdirSync(LOG_DIR, { recursive: true });
  }
}

function getConsoleMethod(level) {
  switch (level) {
    case 'ERROR': return console.error;
    case 'WARN':  return console.warn;
    case 'INFO':  return console.info;
    case 'DEBUG': return console.debug;
    default:      return console.log;
  }
}

function shouldLog(level) {
  return LOG_LEVELS.indexOf(level) >= minLevelIdx;
}

function formatLog(level, message, meta) {
  const time = new Date().toISOString();
  let base = `[${time}] [${level}] ${message}`;
  if (meta && typeof meta === 'object' && Object.keys(meta).length) {
    base += ` | ${JSON.stringify(meta)}`;
  }
  return base;
}

function writeToFile(logString) {
  ensureLogDir();
  fs.appendFile(LOG_PATH, logString + '\n', err => {
    if (err) {
      // Fallback to console if file write fails
      console.error('[Logger] Failed to write log to file:', err);
    }
  });
}

function log(level, message, meta) {
  if (!LOG_LEVELS.includes(level)) {
    console.error(`[Logger] Invalid log level: ${level}. Message: ${message}`);
    return;
  }
  if (!shouldLog(level)) return;

  const output = formatLog(level, message, meta);
  getConsoleMethod(level).call(console, output);
  writeToFile(output);
}

export const info  = (msg, meta) => log('INFO',  msg, meta);
export const warn  = (msg, meta) => log('WARN',  msg, meta);
export const error = (msg, meta) => log('ERROR', msg, meta);
export const debug = (msg, meta) => log('DEBUG', msg, meta);

export const withError = (err, msg = '') => {
  if (!(err instanceof Error)) return error(msg, err);
  error(`${msg}${msg ? ' ' : ''}${err.message}`, { stack: err.stack });
};
