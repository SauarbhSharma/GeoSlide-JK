export interface District {
  id: string;
  sourceName: string;
  displayName: string;
  includedInJkUt: boolean;
  coordinates: [number, number];
  riskLevel: 'Low' | 'Moderate' | 'High' | 'Very High' | 'Critical' | 'Insufficient Data';
}

export const JK_20_DISTRICTS: District[] = [
  { id: 'anantnag', sourceName: 'ANANTNAG', displayName: 'Anantnag', includedInJkUt: true, coordinates: [75.15, 33.73], riskLevel: 'Moderate' },
  { id: 'bandipora', sourceName: 'BANDIPURA', displayName: 'Bandipora', includedInJkUt: true, coordinates: [74.65, 34.42], riskLevel: 'High' },
  { id: 'baramulla', sourceName: 'BARAMULA', displayName: 'Baramulla', includedInJkUt: true, coordinates: [74.35, 34.20], riskLevel: 'High' },
  { id: 'budgam', sourceName: 'BADGAM', displayName: 'Budgam', includedInJkUt: true, coordinates: [74.63, 34.02], riskLevel: 'Low' },
  { id: 'doda', sourceName: 'DODA', displayName: 'Doda', includedInJkUt: true, coordinates: [75.54, 33.14], riskLevel: 'Very High' },
  { id: 'ganderbal', sourceName: 'GANDERBAL', displayName: 'Ganderbal', includedInJkUt: true, coordinates: [74.78, 34.23], riskLevel: 'Moderate' },
  { id: 'jammu', sourceName: 'JAMMU', displayName: 'Jammu', includedInJkUt: true, coordinates: [74.87, 32.73], riskLevel: 'Low' },
  { id: 'kathua', sourceName: 'KATHUA', displayName: 'Kathua', includedInJkUt: true, coordinates: [75.52, 32.37], riskLevel: 'Moderate' },
  { id: 'kishtwar', sourceName: 'KISHTWAR', displayName: 'Kishtwar', includedInJkUt: true, coordinates: [75.77, 33.32], riskLevel: 'Very High' },
  { id: 'kulgam', sourceName: 'KULGAM', displayName: 'Kulgam', includedInJkUt: true, coordinates: [75.02, 33.64], riskLevel: 'Moderate' },
  { id: 'kupwara', sourceName: 'KUPWARA', displayName: 'Kupwara', includedInJkUt: true, coordinates: [74.25, 34.52], riskLevel: 'High' },
  { id: 'poonch', sourceName: 'PUNCH', displayName: 'Poonch', includedInJkUt: true, coordinates: [74.09, 33.77], riskLevel: 'High' },
  { id: 'pulwama', sourceName: 'PULWAMA', displayName: 'Pulwama', includedInJkUt: true, coordinates: [74.92, 33.87], riskLevel: 'Low' },
  { id: 'rajouri', sourceName: 'RAJAURI', displayName: 'Rajouri', includedInJkUt: true, coordinates: [74.31, 33.38], riskLevel: 'High' },
  { id: 'ramban', sourceName: 'RAMBAN', displayName: 'Ramban', includedInJkUt: true, coordinates: [75.24, 33.24], riskLevel: 'Critical' },
  { id: 'reasi', sourceName: 'RIASI', displayName: 'Reasi', includedInJkUt: true, coordinates: [74.83, 33.08], riskLevel: 'High' },
  { id: 'samba', sourceName: 'SAMBA', displayName: 'Samba', includedInJkUt: true, coordinates: [75.12, 32.56], riskLevel: 'Low' },
  { id: 'shopian', sourceName: 'SHUPIYAN', displayName: 'Shopian', includedInJkUt: true, coordinates: [74.83, 33.72], riskLevel: 'Moderate' },
  { id: 'srinagar', sourceName: 'SRINAGAR', displayName: 'Srinagar', includedInJkUt: true, coordinates: [74.80, 34.08], riskLevel: 'Low' },
  { id: 'udhampur', sourceName: 'UDHAMPUR', displayName: 'Udhampur', includedInJkUt: true, coordinates: [75.14, 32.92], riskLevel: 'High' }
];

export const RISK_COLORS = {
  Low: '#22c55e',
  Moderate: '#eab308',
  High: '#f97316',
  'Very High': '#ef4444',
  Critical: '#881337',
  'Insufficient Data': '#64748b'
};
