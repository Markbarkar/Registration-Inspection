import { useState } from 'react';
import { Layout, Card, Input, Button, Table, Space, message, Modal, Statistic, Row, Col, Tag, Divider, Tooltip } from 'antd';
import { CheckCircleOutlined, CloseCircleOutlined, LoadingOutlined, SettingOutlined, DownloadOutlined, DeleteOutlined } from '@ant-design/icons';
import axios from 'axios';
import './App.css';

const { Header, Content } = Layout;
const { TextArea } = Input;

function App() {
  const [emails, setEmails] = useState('');
  const [proxy, setProxy] = useState('');
  const [delay, setDelay] = useState(1);
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState([]);
  const [proxyModalVisible, setProxyModalVisible] = useState(false);
  const [testingProxy, setTestingProxy] = useState(false);

  // API基础地址
  const API_BASE = 'http://localhost:5001';

  // 统计数据
  const stats = {
    total: results.length,
    registered: results.filter(r => r.registered).length,
    unregistered: results.filter(r => !r.registered).length,
    error: results.filter(r => r.status === 'error').length,
  };

  // 开始检测
  const handleCheck = async () => {
    const emailList = emails.trim().split('\n').filter(e => e.trim());
    
    if (emailList.length === 0) {
      message.warning('请输入至少一个邮箱地址');
      return;
    }

    setLoading(true);
    setResults([]);

    try {
      if (emailList.length === 1) {
        // 单个检测
        const response = await axios.post(`${API_BASE}/api/check`, {
          email: emailList[0],
          proxy: proxy || null
        });
        
        if (response.data.success) {
          setResults([response.data.data]);
          message.success('检测完成');
        } else {
          message.error(response.data.error || '检测失败');
        }
      } else {
        // 批量检测
        const response = await axios.post(`${API_BASE}/api/check-batch`, {
          emails: emailList,
          proxy: proxy || null,
          delay: delay
        });
        
        if (response.data.success) {
          setResults(response.data.data);
          message.success(`批量检测完成，共检测 ${response.data.data.length} 个邮箱`);
        } else {
          message.error(response.data.error || '检测失败');
        }
      }
    } catch (error) {
      message.error('请求失败: ' + (error.response?.data?.error || error.message));
    } finally {
      setLoading(false);
    }
  };

  // 测试代理
  const handleTestProxy = async () => {
    if (!proxy.trim()) {
      message.warning('请输入代理地址');
      return;
    }

    setTestingProxy(true);
    try {
      const response = await axios.post(`${API_BASE}/api/test-proxy`, {
        proxy: proxy
      });
      
      if (response.data.success && response.data.valid) {
        message.success('代理连接成功');
      } else {
        message.error('代理连接失败');
      }
    } catch (error) {
      message.error('测试失败: ' + (error.response?.data?.error || error.message));
    } finally {
      setTestingProxy(false);
    }
  };

  // 导出CSV
  const handleExport = () => {
    if (results.length === 0) {
      message.warning('没有可导出的数据');
      return;
    }

    const csvContent = [
      ['邮箱', '状态', '结果', '时间'].join(','),
      ...results.map(r => [
        r.email,
        r.status === 'success' ? '成功' : '失败',
        r.registered ? '已注册' : '未注册',
        new Date(r.timestamp * 1000).toLocaleString()
      ].join(','))
    ].join('\n');

    const blob = new Blob(['\ufeff' + csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = `检测结果_${new Date().getTime()}.csv`;
    link.click();
    message.success('导出成功');
  };

  // 清空结果
  const handleClear = () => {
    setResults([]);
    message.success('已清空结果');
  };

  // 表格列定义
  const columns = [
    {
      title: '序号',
      key: 'index',
      width: 70,
      render: (_, __, index) => index + 1,
    },
    {
      title: '邮箱地址',
      dataIndex: 'email',
      key: 'email',
      ellipsis: true,
    },
    {
      title: '检测状态',
      dataIndex: 'status',
      key: 'status',
      width: 100,
      render: (status) => (
        <Tag color={status === 'success' ? 'success' : 'error'}>
          {status === 'success' ? '成功' : '失败'}
        </Tag>
      ),
    },
    {
      title: '注册状态',
      dataIndex: 'registered',
      key: 'registered',
      width: 120,
      render: (registered, record) => {
        if (record.status !== 'success') {
          return <Tag color="default">未知</Tag>;
        }
        return registered ? (
          <Tag icon={<CheckCircleOutlined />} color="success">已注册</Tag>
        ) : (
          <Tag icon={<CloseCircleOutlined />} color="default">未注册</Tag>
        );
      },
    },
    {
      title: '详细信息',
      dataIndex: 'message',
      key: 'message',
      ellipsis: {
        showTitle: false,
      },
      render: (message) => (
        <Tooltip placement="topLeft" title={message}>
          {message}
        </Tooltip>
      ),
    },
    {
      title: '检测时间',
      dataIndex: 'timestamp',
      key: 'timestamp',
      width: 180,
      render: (timestamp) => new Date(timestamp * 1000).toLocaleString(),
    },
  ];

  return (
    <Layout className="layout">
      <Header className="header">
        <div className="header-content">
          <h1 className="title">网站注册检测系统</h1>
          <div className="subtitle">Stir.com 邮箱注册状态检测</div>
        </div>
      </Header>
      
      <Content className="content">
        <div className="container">
          {/* 输入区域 */}
          <Card 
            title="检测设置" 
            className="input-card"
            extra={
              <Button 
                icon={<SettingOutlined />} 
                onClick={() => setProxyModalVisible(true)}
              >
                代理设置
              </Button>
            }
          >
            <Space direction="vertical" style={{ width: '100%' }} size="large">
              <div>
                <div className="label">邮箱地址（每行一个）</div>
                <TextArea
                  rows={8}
                  placeholder="请输入要检测的邮箱地址，每行一个&#10;例如：&#10;example1@gmail.com&#10;example2@gmail.com"
                  value={emails}
                  onChange={(e) => setEmails(e.target.value)}
                  disabled={loading}
                />
              </div>
              
              <Button
                type="primary"
                size="large"
                block
                onClick={handleCheck}
                loading={loading}
                icon={loading ? <LoadingOutlined /> : null}
              >
                {loading ? '检测中...' : '开始检测'}
              </Button>
            </Space>
          </Card>

          {/* 统计区域 */}
          {results.length > 0 && (
            <Card className="stats-card">
              <Row gutter={16}>
                <Col span={6}>
                  <Statistic 
                    title="总计" 
                    value={stats.total} 
                    valueStyle={{ color: '#1890ff' }}
                  />
                </Col>
                <Col span={6}>
                  <Statistic 
                    title="已注册" 
                    value={stats.registered} 
                    valueStyle={{ color: '#52c41a' }}
                    prefix={<CheckCircleOutlined />}
                  />
                </Col>
                <Col span={6}>
                  <Statistic 
                    title="未注册" 
                    value={stats.unregistered} 
                    valueStyle={{ color: '#8c8c8c' }}
                    prefix={<CloseCircleOutlined />}
                  />
                </Col>
                <Col span={6}>
                  <Statistic 
                    title="检测失败" 
                    value={stats.error} 
                    valueStyle={{ color: '#ff4d4f' }}
                  />
                </Col>
              </Row>
              
              <Divider />
              
              <Space>
                <Button 
                  icon={<DownloadOutlined />} 
                  onClick={handleExport}
                >
                  导出CSV
                </Button>
                <Button 
                  icon={<DeleteOutlined />} 
                  onClick={handleClear}
                  danger
                >
                  清空结果
                </Button>
              </Space>
            </Card>
          )}

          {/* 结果表格 */}
          {results.length > 0 && (
            <Card title="检测结果" className="result-card">
              <Table
                columns={columns}
                dataSource={results}
                rowKey={(record) => record.email + record.timestamp}
                pagination={{
                  pageSize: 10,
                  showSizeChanger: true,
                  showTotal: (total) => `共 ${total} 条记录`,
                }}
              />
            </Card>
          )}
        </div>
      </Content>

      {/* 代理设置模态框 */}
      <Modal
        title="代理设置"
        open={proxyModalVisible}
        onCancel={() => setProxyModalVisible(false)}
        footer={[
          <Button key="test" onClick={handleTestProxy} loading={testingProxy}>
            测试连接
          </Button>,
          <Button key="close" onClick={() => setProxyModalVisible(false)}>
            关闭
          </Button>,
        ]}
      >
        <Space direction="vertical" style={{ width: '100%' }} size="middle">
          <div>
            <div className="label">代理地址</div>
            <Input
              placeholder="例如: http://127.0.0.1:7890 或 socks5://127.0.0.1:1080"
              value={proxy}
              onChange={(e) => setProxy(e.target.value)}
            />
            <div className="hint">留空表示不使用代理</div>
          </div>
          
          <div>
            <div className="label">批量检测延迟（秒）</div>
            <Input
              type="number"
              min={0}
              step={0.5}
              value={delay}
              onChange={(e) => setDelay(parseFloat(e.target.value) || 0)}
            />
            <div className="hint">批量检测时每个请求之间的延迟时间，避免请求过快</div>
          </div>
        </Space>
      </Modal>
    </Layout>
  );
}

export default App;
