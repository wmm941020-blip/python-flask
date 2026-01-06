import { http } from "@/utils/http";

type Result = {
  success: boolean;
  data?: any;
  message?: string;
};

// User API
export const getUserList = (params?: object) => {
  return http.request<Result>("get", "/api/users", { params });
};

export const createUser = (data?: object) => {
  return http.request<Result>("post", "/api/users", { data });
};

export const updateUser = (id: number, data?: object) => {
  return http.request<Result>("put", `/api/users/${id}`, { data });
};

export const deleteUser = (id: number) => {
  return http.request<Result>("delete", `/api/users/${id}`);
};

// Role API
export const getRoleList = (params?: object) => {
  return http.request<Result>("get", "/api/roles", { params });
};

export const createRole = (data?: object) => {
  return http.request<Result>("post", "/api/roles", { data });
};

export const updateRole = (id: number, data?: object) => {
  return http.request<Result>("put", `/api/roles/${id}`, { data });
};

export const deleteRole = (id: number) => {
  return http.request<Result>("delete", `/api/roles/${id}`);
};

// Menu API
export const getMenuList = (params?: object) => {
  return http.request<Result>("get", "/api/menus", { params });
};

export const createMenu = (data?: object) => {
  return http.request<Result>("post", "/api/menus", { data });
};

export const updateMenu = (id: number, data?: object) => {
  return http.request<Result>("put", `/api/menus/${id}`, { data });
};

export const deleteMenu = (id: number) => {
  return http.request<Result>("delete", `/api/menus/${id}`);
};

// Position API
export const getPositionList = (params?: object) => {
  return http.request<Result>("get", "/api/positions", { params });
};

export const createPosition = (data?: object) => {
  return http.request<Result>("post", "/api/positions", { data });
};

export const updatePosition = (id: number, data?: object) => {
  return http.request<Result>("put", `/api/positions/${id}`, { data });
};

export const deletePosition = (id: number) => {
  return http.request<Result>("delete", `/api/positions/${id}`);
};
