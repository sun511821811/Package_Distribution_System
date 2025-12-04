import {
    DeleteOutlined,
    PlayCircleOutlined,
    PlusOutlined,
    PauseCircleOutlined,
} from "@ant-design/icons";
import {
    Button,
    Card,
    Form,
    InputNumber,
    Modal,
    Select,
    Space,
    Switch,
    Table,
    Tag,
    message,
} from "antd";
import React, { useEffect, useState } from "react";
import {
    createScheduledTask,
    deleteScheduledTask,
    getPackages,
    getScheduledTasks,
    runScheduledTask,
    pauseScheduledTask,
    resumeScheduledTask,
} from "../services/authService";

interface ScheduledTask {
    id: number;
    package_id: string;
    package_name: string;
    interval_seconds: number;
    last_run_at: string | null;
    next_run_at: string;
    is_active: boolean;
}

interface PackageData {
    id: string;
    name: string;
}

const TaskManagement: React.FC = () => {
    const [tasks, setTasks] = useState<ScheduledTask[]>([]);
    const [packages, setPackages] = useState<PackageData[]>([]);
    const [loading, setLoading] = useState(false);
    const [isModalVisible, setIsModalVisible] = useState(false);
    const [form] = Form.useForm();

    const fetchData = async () => {
        setLoading(true);
        try {
            const [tasksRes, packagesRes] = await Promise.all([
                getScheduledTasks(),
                getPackages(),
            ]);
            setTasks(tasksRes.data.data);
            setPackages(packagesRes.data.data);
        } catch {
            message.error("获取数据失败");
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchData();
    }, []);

    const handleCreate = async (values: any) => {
        try {
            await createScheduledTask(values);
            message.success("创建任务成功");
            setIsModalVisible(false);
            form.resetFields();
            fetchData();
        } catch (error: any) {
            message.error(
                "创建失败: " + (error.response?.data?.detail || "未知错误")
            );
        }
    };

    const handleDelete = async (id: string) => {
        try {
            await deleteScheduledTask(id);
            message.success("删除成功");
            fetchData();
        } catch {
            message.error("删除失败");
        }
    };

    const handleRunNow = async (id: string) => {
        try {
            await runScheduledTask(id);
            message.success("已触发任务");
            fetchData();
        } catch {
            message.error("触发失败");
        }
    };

    const handleToggleActive = async (record: ScheduledTask) => {
        try {
            if (record.is_active) {
                await pauseScheduledTask(record.id.toString());
                message.success("任务已暂停");
            } else {
                await resumeScheduledTask(record.id.toString());
                message.success("任务已恢复");
            }
            fetchData();
        } catch {
            message.error("操作失败");
        }
    };

    const columns = [
        {
            title: "ID",
            dataIndex: "id",
            key: "id",
            width: 80,
        },
        {
            title: "包名称 (ID)",
            key: "package",
            render: (record: ScheduledTask) => (
                <span>
                    {record.package_name} <br />
                    <span style={{ fontSize: "12px", color: "#888" }}>
                        {record.package_id}
                    </span>
                </span>
            ),
        },
        {
            title: "间隔 (秒)",
            dataIndex: "interval_seconds",
            key: "interval_seconds",
        },
        {
            title: "状态",
            dataIndex: "is_active",
            key: "is_active",
            render: (active: boolean) => (
                <Tag color={active ? "green" : "red"}>
                    {active ? "启用" : "禁用"}
                </Tag>
            ),
        },
        {
            title: "上次运行",
            dataIndex: "last_run_at",
            key: "last_run_at",
            render: (val: string) =>
                val ? new Date(val).toLocaleString() : "从未",
        },
        {
            title: "下次运行",
            dataIndex: "next_run_at",
            key: "next_run_at",
            render: (val: string) => new Date(val).toLocaleString(),
        },
        {
            title: "操作",
            key: "action",
            render: (record: ScheduledTask) => (
                <Space>
                    <Button
                        type="link"
                        icon={record.is_active ? <PauseCircleOutlined /> : <PlayCircleOutlined />}
                        size="small"
                        onClick={() => handleToggleActive(record)}
                    >
                        {record.is_active ? "暂停" : "恢复"}
                    </Button>
                    <Button
                        icon={<PlayCircleOutlined />}
                        size="small"
                        onClick={() => handleRunNow(record.id.toString())}
                    >
                        立即运行
                    </Button>
                    <Button
                        danger
                        icon={<DeleteOutlined />}
                        size="small"
                        onClick={() => handleDelete(record.id.toString())}
                    >
                        删除
                    </Button>
                </Space>
            ),
        },
    ];

    return (
        <Card
            title="定时任务管理"
            extra={
                <Button
                    type="primary"
                    icon={<PlusOutlined />}
                    onClick={() => setIsModalVisible(true)}
                >
                    新建任务
                </Button>
            }
        >
            <Table
                columns={columns}
                dataSource={tasks}
                rowKey="id"
                loading={loading}
            />

            <Modal
                title="新建定时任务"
                open={isModalVisible}
                onOk={() => form.submit()}
                onCancel={() => setIsModalVisible(false)}
            >
                <Form form={form} layout="vertical" onFinish={handleCreate}>
                    <Form.Item
                        name="package_id"
                        label="选择包"
                        rules={[{ required: true, message: "请选择包" }]}
                    >
                        <Select
                            showSearch
                            optionFilterProp="children"
                            filterOption={(input, option) =>
                                (option?.label ?? "")
                                    .toLowerCase()
                                    .includes(input.toLowerCase())
                            }
                            options={packages.map((pkg) => ({
                                value: pkg.id,
                                label: `${pkg.name} (${pkg.id})`,
                            }))}
                        />
                    </Form.Item>
                    <Form.Item
                        name="interval_seconds"
                        label="间隔时间 (秒)"
                        rules={[{ required: true, message: "请输入间隔时间" }]}
                        initialValue={3600}
                    >
                        <InputNumber min={60} style={{ width: "100%" }} />
                    </Form.Item>
                    <Form.Item
                        name="is_active"
                        label="是否启用"
                        valuePropName="checked"
                        initialValue={true}
                    >
                        <Switch />
                    </Form.Item>
                </Form>
            </Modal>
        </Card>
    );
};

export default TaskManagement;
