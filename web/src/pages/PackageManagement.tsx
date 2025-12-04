import {
    DeleteOutlined,
    DownloadOutlined,
    DownOutlined,
    PlusOutlined,
    ReloadOutlined,
    UploadOutlined,
} from "@ant-design/icons";
import type { MenuProps } from "antd";
import {
    Button,
    Dropdown,
    Form,
    Input,
    message,
    Modal,
    Popconfirm,
    Space,
    Table,
    Tag,
    Typography,
    Upload,
} from "antd";
import React, { useEffect, useState } from "react";
import {
    deletePackage,
    getPackages,
    retryPackage,
    uploadPackage,
} from "../services/authService";

const { Paragraph } = Typography;

interface PackageData {
    id: string;
    name: string;
    version: string;
    description?: string;
    status: string;
    is_distributing: boolean;
    download_url?: string;
    original_download_url?: string;
}

const PackageManagement: React.FC = () => {
    const [data, setData] = useState<PackageData[]>([]);
    const [isModalVisible, setIsModalVisible] = useState(false);
    const [isReplaceModalVisible, setIsReplaceModalVisible] = useState(false);
    const [selectedPackageId, setSelectedPackageId] = useState<string | null>(
        null
    );
    const [loading, setLoading] = useState(false);
    const [form] = Form.useForm();
    const [replaceForm] = Form.useForm();

    const fetchPackages = async () => {
        try {
            const res = await getPackages();
            setData(res.data.data);
        } catch {
            message.error("获取包列表失败");
        }
    };

    useEffect(() => {
        fetchPackages();
    }, []);

    const handleUpload = async (values: any) => {
        setLoading(true);
        const formData = new FormData();
        formData.append("name", values.name);
        formData.append("version", values.version);
        if (values.description) {
            formData.append("description", values.description);
        }
        if (values.file && values.file.fileList.length > 0) {
            formData.append("file", values.file.fileList[0].originFileObj);
        } else {
            message.error("请选择文件");
            setLoading(false);
            return;
        }

        try {
            await uploadPackage(formData);
            message.success("包上传成功，开始处理");
            setIsModalVisible(false);
            form.resetFields();
            fetchPackages();
        } catch (error) {
            const err = error as { response?: { data?: { detail?: string } } };
            const msg = err.response?.data?.detail || "上传失败";
            message.error(msg);
        } finally {
            setLoading(false);
        }
    };

    const handleReplaceOriginal = async (values: any) => {
        if (!selectedPackageId) return;
        setLoading(true);

        const formData = new FormData();
        formData.append("version", values.version);
        if (values.file && values.file.fileList.length > 0) {
            formData.append("file", values.file.fileList[0].originFileObj);
        } else {
            message.error("请选择文件");
            setLoading(false);
            return;
        }

        try {
            await import("../services/authService").then((mod) =>
                mod.replaceOriginalPackage(selectedPackageId, formData)
            );
            message.success("原包替换成功，已重新开始处理");
            setIsReplaceModalVisible(false);
            replaceForm.resetFields();
            setSelectedPackageId(null);
            fetchPackages();
        } catch (error) {
            const err = error as { response?: { data?: { detail?: string } } };
            const msg = err.response?.data?.detail || "替换失败";
            message.error(msg);
        } finally {
            setLoading(false);
        }
    };

    const handleDelete = async (id: string) => {
        try {
            await deletePackage(id);
            message.success("删除成功");
            fetchPackages();
        } catch (error) {
            const err = error as {
                response?: { data?: { detail?: string; message?: string } };
            };
            const msg =
                err.response?.data?.detail ||
                err.response?.data?.message ||
                "删除失败";
            message.error(msg);
        }
    };

    const handleRetry = async (id: string) => {
        try {
            await retryPackage(id);
            message.success("已触发重试");
            fetchPackages();
        } catch (error) {
            const err = error as { response?: { data?: { detail?: string } } };
            message.error(
                "重试失败: " + (err.response?.data?.detail || "未知错误")
            );
        }
    };

    const handleDownload = (url?: string) => {
        if (url) {
            window.open(url, "_blank");
        } else {
            message.warning("下载链接不可用");
        }
    };

    const columns = [
        {
            title: "ID",
            dataIndex: "id",
            key: "id",
            width: 60,
        },
        {
            title: "名称",
            dataIndex: "name",
            key: "name",
        },
        {
            title: "版本",
            dataIndex: "version",
            key: "version",
        },
        {
            title: "下载链接",
            key: "download",
            width: 300,
            render: (_: unknown, record: PackageData) => (
                <Space
                    direction="vertical"
                    size="small"
                    style={{ width: "100%" }}
                >
                    {record.original_download_url && (
                        <div
                            style={{
                                display: "flex",
                                alignItems: "center",
                                gap: 8,
                            }}
                        >
                            <span
                                style={{ whiteSpace: "nowrap", minWidth: 40 }}
                            >
                                原包:
                            </span>
                            <Paragraph
                                copyable={{
                                    text: record.original_download_url,
                                }}
                                ellipsis={{
                                    rows: 1,
                                    expandable: false,
                                    symbol: "...",
                                }}
                                style={{ margin: 0, flex: 1, width: 200 }}
                            >
                                <a
                                    href={record.original_download_url}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                >
                                    {record.original_download_url}
                                </a>
                            </Paragraph>
                        </div>
                    )}
                    {record.download_url && (
                        <div
                            style={{
                                display: "flex",
                                alignItems: "center",
                                gap: 8,
                            }}
                        >
                            <span
                                style={{ whiteSpace: "nowrap", minWidth: 40 }}
                            >
                                处理包:
                            </span>
                            <Paragraph
                                copyable={{ text: record.download_url }}
                                ellipsis={{
                                    rows: 1,
                                    expandable: false,
                                    symbol: "...",
                                }}
                                style={{ margin: 0, flex: 1, width: 200 }}
                            >
                                <a
                                    href={record.download_url}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                >
                                    {record.download_url}
                                </a>
                            </Paragraph>
                        </div>
                    )}
                </Space>
            ),
        },
        {
            title: "状态",
            dataIndex: "status",
            key: "status",
            render: (status: string) => {
                let color = "default";
                let text = status;
                if (status === "processed_success") {
                    color = "success";
                    text = "处理成功";
                }
                if (status === "processed_failed") {
                    color = "error";
                    text = "处理失败";
                }
                if (status === "processing") {
                    color = "processing";
                    text = "处理中";
                }
                if (status === "pending") {
                    color = "warning";
                    text = "等待处理";
                }
                return <Tag color={color}>{text}</Tag>;
            },
        },
        {
            title: "分发中",
            dataIndex: "is_distributing",
            key: "is_distributing",
            render: (val: boolean) =>
                val ? <Tag color="green">是</Tag> : <Tag color="red">否</Tag>,
        },
        {
            title: "描述",
            dataIndex: "description",
            key: "description",
            width: 200,
            render: (text: string) => (
                <Paragraph
                    ellipsis={{ rows: 1, tooltip: true }}
                    style={{ marginBottom: 0 }}
                >
                    {text}
                </Paragraph>
            ),
        },
        {
            title: "操作",
            key: "action",
            width: 150,
            render: (_: unknown, record: PackageData) => {
                const items: MenuProps["items"] = [
                    {
                        key: "replace",
                        label: "替换原包",
                        icon: <UploadOutlined />,
                        onClick: () => {
                            setSelectedPackageId(record.id);
                            setIsReplaceModalVisible(true);
                        },
                    },
                    {
                        key: "download",
                        label: "下载",
                        icon: <DownloadOutlined />,
                        disabled: !record.download_url,
                        onClick: () => handleDownload(record.download_url),
                    },
                    {
                        key: "retry",
                        label: "重试",
                        icon: <ReloadOutlined />, // Use ReloadOutlined instead of PlayCircleOutlined
                        onClick: () => handleRetry(record.id),
                    },
                    {
                        type: "divider",
                    },
                    {
                        key: "delete",
                        label: (
                            <Popconfirm
                                title="确定删除吗?"
                                onConfirm={() => handleDelete(record.id)}
                                okText="是"
                                cancelText="否"
                            >
                                <span style={{ color: "red" }}>删除</span>
                            </Popconfirm>
                        ),
                        icon: <DeleteOutlined style={{ color: "red" }} />,
                    },
                ];

                return (
                    <Dropdown menu={{ items }} trigger={["click"]}>
                        <Button>
                            操作 <DownOutlined />
                        </Button>
                    </Dropdown>
                );
            },
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
                <h2>包管理</h2>
                <div>
                    <Button
                        icon={<ReloadOutlined />}
                        onClick={fetchPackages}
                        style={{ marginRight: 8 }}
                    >
                        刷新
                    </Button>
                    <Button
                        type="primary"
                        icon={<PlusOutlined />}
                        onClick={() => setIsModalVisible(true)}
                    >
                        上传包
                    </Button>
                </div>
            </div>
            <Table columns={columns} dataSource={data} rowKey="id" />

            <Modal
                title="上传包"
                open={isModalVisible}
                onCancel={() => setIsModalVisible(false)}
                footer={null}
            >
                <Form form={form} layout="vertical" onFinish={handleUpload}>
                    <Form.Item
                        name="name"
                        label="包名称"
                        rules={[
                            {
                                required: true,
                                message: "请输入包名称!",
                            },
                        ]}
                    >
                        <Input />
                    </Form.Item>
                    <Form.Item
                        name="version"
                        label="版本号"
                        rules={[
                            {
                                required: true,
                                message: "请输入版本号!",
                            },
                        ]}
                    >
                        <Input />
                    </Form.Item>
                    <Form.Item name="description" label="描述">
                        <Input.TextArea />
                    </Form.Item>
                    <Form.Item
                        name="file"
                        label="APK 文件"
                        rules={[
                            {
                                required: true,
                                message: "请选择文件!",
                            },
                        ]}
                    >
                        <Upload
                            beforeUpload={() => false}
                            maxCount={1}
                            accept=".apk"
                        >
                            <Button icon={<UploadOutlined />}>选择 APK</Button>
                        </Upload>
                    </Form.Item>
                    <Form.Item>
                        <Button
                            type="primary"
                            htmlType="submit"
                            loading={loading}
                            block
                        >
                            上传
                        </Button>
                    </Form.Item>
                </Form>
            </Modal>

            <Modal
                title="替换原包"
                open={isReplaceModalVisible}
                onCancel={() => {
                    setIsReplaceModalVisible(false);
                    replaceForm.resetFields();
                    setSelectedPackageId(null);
                }}
                footer={null}
            >
                <Form
                    form={replaceForm}
                    layout="vertical"
                    onFinish={handleReplaceOriginal}
                >
                    <Form.Item
                        name="version"
                        label="新版本号"
                        rules={[
                            {
                                required: true,
                                message: "请输入新版本号!",
                            },
                        ]}
                    >
                        <Input />
                    </Form.Item>
                    <Form.Item
                        name="file"
                        label="APK 文件"
                        rules={[
                            {
                                required: true,
                                message: "请选择文件!",
                            },
                        ]}
                    >
                        <Upload
                            beforeUpload={() => false}
                            maxCount={1}
                            accept=".apk"
                        >
                            <Button icon={<UploadOutlined />}>
                                选择新 APK
                            </Button>
                        </Upload>
                    </Form.Item>
                    <Form.Item>
                        <Button
                            type="primary"
                            htmlType="submit"
                            loading={loading}
                            block
                        >
                            替换并重新处理
                        </Button>
                    </Form.Item>
                </Form>
            </Modal>
        </div>
    );
};

export default PackageManagement;
