import api from "../utils/api";

export const login = async (data: any) => {
    const formData = new FormData();
    formData.append("username", data.username);
    formData.append("password", data.password);
    return api.post("/admin/login", formData);
};

export const createPackage = async (data: any) => {
    return api.post("/admin/packages", data);
};

export const uploadPackage = async (formData: FormData) => {
    return api.post("/admin/packages/upload", formData, {
        headers: {
            "Content-Type": "multipart/form-data",
        },
        timeout: 600000, // 10 minutes
    });
};

export const getPackages = async () => {
    return api.get("/admin/packages");
};

export const getUsers = async () => {
    return api.get("/admin/users");
};

export const createUser = async (data: any) => {
    return api.post("/admin/users", data);
};

export const retryPackage = async (id: string) => {
    return api.post(`/admin/packages/${id}/retry`);
};

export const deletePackage = async (id: string) => {
    return api.delete(`/admin/packages/${id}`);
};

export const getScheduledTasks = async () => {
    return api.get("/admin/tasks/scheduled");
};

export const createScheduledTask = async (data: any) => {
    return api.post("/admin/tasks/scheduled", data);
};

export const deleteScheduledTask = async (id: string) => {
    return api.delete(`/admin/tasks/scheduled/${id}`);
};

export const runScheduledTask = async (id: string) => {
    return api.post(`/admin/tasks/scheduled/${id}/run`);
};

export const pauseScheduledTask = async (id: string) => {
    return api.post(`/admin/tasks/scheduled/${id}/pause`);
};

export const resumeScheduledTask = async (id: string) => {
    return api.post(`/admin/tasks/scheduled/${id}/resume`);
};

export const replaceOriginalPackage = async (
    id: string,
    formData: FormData
) => {
    return api.post(`/admin/packages/${id}/replace-original`, formData, {
        headers: {
            "Content-Type": "multipart/form-data",
        },
        timeout: 600000, // 10 minutes
    });
};
