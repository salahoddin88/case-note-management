// API Types matching Django Ninja schemas

export interface Client {
  id: string;
  first_name: string;
  last_name: string;
  client_id: string;
}

export interface ClientDetail extends Client {
  assigned_caseworker_name: string;
}

export interface CaseNote {
  id: string;
  content: string;
  interaction_type: string;
  created_at: string;
  created_by: {
    id: string;
    name: string;
  };
}

export interface CaseNoteCreateRequest {
  client_id: string;
  content: string;
  interaction_type: string;
}

export interface CaseNoteCreateResponse {
  id: string;
  created_at: string;
  success: boolean;
}

export interface CaseNotesListResponse {
  case_notes: CaseNote[];
}

export interface ClientSearchResponse {
  results: Client[];
}

// Interaction types for the dropdown
export const INTERACTION_TYPES = [
  { value: 'phone', label: 'Phone Call' },
  { value: 'in-person', label: 'In-Person Meeting' },
  { value: 'email', label: 'Email' },
  { value: 'video', label: 'Video Call' },
  { value: 'other', label: 'Other' },
] as const;

export type InteractionType = typeof INTERACTION_TYPES[number]['value']; 