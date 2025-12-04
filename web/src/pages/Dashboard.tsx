import React from 'react';
import { Card, Col, Row, Statistic } from 'antd';
import { AppstoreOutlined, UserOutlined, CloudServerOutlined } from '@ant-design/icons';

const Dashboard: React.FC = () => {
  return (
    <div>
        <h2>首页看板</h2>
        <Row gutter={16}>
            <Col span={8}>
            <Card>
                <Statistic
                title="总包数量"
                value={12} // Placeholder
                prefix={<AppstoreOutlined />}
                />
            </Card>
            </Col>
            <Col span={8}>
            <Card>
                <Statistic
                title="活跃用户"
                value={3} // Placeholder
                prefix={<UserOutlined />}
                />
            </Card>
            </Col>
            <Col span={8}>
            <Card>
                <Statistic
                title="已处理任务"
                value={8} // Placeholder
                prefix={<CloudServerOutlined />}
                />
            </Card>
            </Col>
        </Row>
        
        <div style={{ marginTop: 24 }}>
            <Card title="系统状态">
                <p>系统运行正常。</p>
                <p>环境: 生产环境</p>
            </Card>
        </div>
    </div>
  );
};

export default Dashboard;
