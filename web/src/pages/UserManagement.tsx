import { PlusOutlined } from "@ant-design/icons";
import { Button, Form, Input, message, Modal, Select, Table, Tag } from "antd";
import React, { useEffect, useState } from "react";
import { createUser, getUsers } from "../services/authService";

const { Option } = Select;

const UserManagement: React.FC = () => {
    const [data, setData] = useState<any[]>([]);
    const [isModalVisible, setIsModalVisible] = useState(false);
    const [loading, setLoading] = useState(false);
    const [form] = Form.useForm();

    const fetchData = async () => {
        try {
            const res = await getUsers();
            setData(res.data.data);
        } catch (error) {
            console.error(error);
        }
    };

    useEffect(() => {
        fetchData();
    }, []);

    const handleCreate = async (values: any) => {
        setLoading(true);
        try {
            await createUser(values);
            message.success("用户创建成功");
            setIsModalVisible(false);
            form.resetFields();
            fetchData();
        } catch (error: any) {
            const msg = error.response?.data?.detail || "创建用户失败";
            message.error(msg);
        } finally {
            setLoading(false);
        }
    };

    const columns = [
        {
            title: "ID",
            dataIndex: "id",
            key: "id",
        },
        {
            title: "用户名",
            dataIndex: "username",
            key: "username",
        },
        {
            title: "角色",
            dataIndex: "role",
            key: "role",
            render: (role: string) => (
                <Tag color={role === "admin" ? "gold" : "blue"}>
                    {role.toUpperCase()}
                </Tag>
            ),
        },
        {
            title: "创建时间",
            dataIndex: "created_at",
            key: "created_at",
        },
    ];

    return (
        <div>
            <div
                style={{
                    marginBottom: 16,
                    display: "flex",
                    justifyContent: "space-between",
                }}
            >
                <h2>用户管理</h2>
                <Button
                    type="primary"
                    icon={<PlusOutlined />}
                    onClick={() => setIsModalVisible(true)}
                >
                    创建用户
                </Button>
            </div>
            <Table columns={columns} dataSource={data} rowKey="id" />

            <Modal
                title="创建用户"
                open={isModalVisible}
                onCancel={() => setIsModalVisible(false)}
                footer={null}
            >
                <Form form={form} layout="vertical" onFinish={handleCreate}>
                    <Form.Item
                        name="username"
                        label="用户名"
                        rules={[
                            {
                                required: true,
                                message: "请输入用户名!",
                            },
                        ]}
                    >
                        <Input />
                    </Form.Item>
                    <Form.Item
                        name="password"
                        label="密码"
                        rules={[
                            {
                                required: true,
                                message: "请输入密码!",
                            },
                        ]}
                    >
                        <Input.Password />
                    </Form.Item>
                    <Form.Item name="role" label="角色" initialValue="operator">
                        <Select>
                            <Option value="admin">管理员</Option>
                            <Option value="operator">操作员</Option>
                        </Select>
                    </Form.Item>
                    <Form.Item>
                        <Button
                            type="primary"
                            htmlType="submit"
                            loading={loading}
                            block
                        >
                            创建
                        </Button>
                    </Form.Item>
                </Form>
            </Modal>
        </div>
    );
};

export default UserManagement;
