import { Button, Card, Form, Input, Switch, message } from "antd";
import React from "react";

const Settings: React.FC = () => {
    const [form] = Form.useForm();

    const onFinish = (values: any) => {
        console.log("Success:", values);
        message.success("设置已保存 (演示功能)");
    };

    return (
        <div>
            <h2>系统设置</h2>
            <Card title="通用设置">
                <Form
                    form={form}
                    layout="vertical"
                    onFinish={onFinish}
                    initialValues={{
                        siteName: "包分发系统",
                        maintenanceMode: false,
                        cdnDomain: "dl.yourdomain.com",
                    }}
                >
                    <Form.Item label="站点名称" name="siteName">
                        <Input />
                    </Form.Item>
                    <Form.Item label="CDN 域名" name="cdnDomain">
                        <Input />
                    </Form.Item>
                    <Form.Item
                        label="维护模式"
                        name="maintenanceMode"
                        valuePropName="checked"
                    >
                        <Switch />
                    </Form.Item>
                    <Form.Item>
                        <Button type="primary" htmlType="submit">
                            保存设置
                        </Button>
                    </Form.Item>
                </Form>
            </Card>
        </div>
    );
};

export default Settings;
