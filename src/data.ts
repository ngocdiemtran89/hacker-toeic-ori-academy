import type { Unit } from './types';

// Dynamically import all JSON files inside content/units directory using Vite's glob import
const modules = import.meta.glob('./content/units/*.json', { eager: true }) as Record<string, { default: any }>;

const units: Unit[] = Object.keys(modules)
  .sort()
  .map(key => modules[key].default as Unit);

export function getAllUnits(): Unit[] {
  return units;
}

export function getUnit(id: string): Unit | undefined {
  return units.find(u => u.id === id);
}
