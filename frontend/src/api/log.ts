import { http } from "@/utils/http";

type Result = {
  success: boolean;
  data?: any;
  message?: string;
};

export const getLogList = (params?: object) => {
  return http.request<Result>("get", "/api/logs", { params });
};

export const createLog = (data?: object) => {
  return http.request<Result>("post", "/api/logs", { data });
};

export const exportLogs = (data: object = {}) => {
  return http.request<Result>("post", "/api/logs/export", { data });
};

export const getExportStatus = (taskId: string) => {
  return http.request<Result>("get", `/api/logs/export/status/${taskId}`);
};
