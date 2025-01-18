export interface DimensionContextType {
  isLandscape: boolean;
  plus500h: boolean;
  plus768h: boolean;
  plus1080h: boolean;
  plus375: boolean;
  plus425: boolean;
  plus550: boolean;
  plus768: boolean;
  plus1024: boolean;
  plus1440: boolean;
}
export interface UserContextType {
  theme: "light" | "dark";
}

export interface AuthResponse {
  detail: string;
}
export interface ServerResponse {
  status: number;
  message: string;
}

// # ---------------------------- Login, Register ----------------------------#
export interface LoginGet {
  username: string;
  password: string;
}
export interface RegisterGet {
  username: string;
  email: string;
  password: string;
}
export interface ChangePasswordGet {
  new_password: string;
  old_password: string;
}
export interface ContactFormGet {
  name: string;
  email: string;
  subject: string;
  message: string;
}
export interface Token {
  access: string;
  refresh: string;
}

// # ---------------------------- User ----------------------------#
export interface User {
  id: number;
  last_login: string;
  is_superuser: boolean;
  username: string;
  first_name: string;
  last_name: string;
  email: string;
  is_staff: boolean;
  is_active: boolean;
  date_joined: string;
}
export interface UserTasks extends User {
  tasks: Task[];
}
export interface Task {
  id: number;
  title: string;
  description: string;
  completed: boolean;
  due_date: string | null;
  owner_id: number;
  updated_at: string;
  created_at: string;
}
export interface UsersGet {
  type: "default" | "user_tasks";
}
export interface TasksGet {
  page: number;
  page_size: number;
  sort_by: "title" | "due_date" | "completed" | "created_at" | "updated_at";
  sort_type: "asc" | "desc";
}
export interface TasksIn {
  total_tasks: number;
  tasks: Task[];
}
export interface TasksIdGet {
  id: number;
}
