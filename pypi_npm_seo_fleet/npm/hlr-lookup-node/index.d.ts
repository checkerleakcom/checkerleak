export interface PhoneVerificationResult {
  phone: string;
  carrier: string;
  line_type: string;
  reachability_score: number;
  is_valid: boolean;
  whatsapp?: Record<string, any>;
  telegram?: Record<string, any>;
}

export class CheckerLeakClient {
  constructor(apiKey?: string, baseUrl?: string);
  verify(phone: string): Promise<PhoneVerificationResult>;
}

export function checkPhone(phone: string, apiKey?: string): Promise<PhoneVerificationResult>;
