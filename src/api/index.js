import axios from 'axios'
import { ElMessage } from 'element-plus'

// 创建axios实例
const api = axios.create({
  baseURL: '/api',
  timeout: 30000  // 增加到30秒
})

// 响应拦截器
api.interceptors.response.use(
  response => {
    const { code, message, data } = response.data
    if (code === 200) {
      return data
    } else {
      ElMessage.error(message || '请求失败')
      return Promise.reject(new Error(message))
    }
  },
  error => {
    console.error('API请求错误:', error)
    let errorMessage = '网络错误'
    
    if (error.code === 'ECONNABORTED') {
      errorMessage = '请求超时，请检查网络连接'
    } else if (error.response) {
      errorMessage = `服务器错误: ${error.response.status}`
    } else if (error.request) {
      errorMessage = '无法连接到服务器'
    }
    
    ElMessage.error(errorMessage)
    return Promise.reject(error)
  }
)

// API方法
export const judgeApi = {
  // 评委登录
  login: (username, password) => 
    api.post(`/judge/login?username=${username}&password=${password}`),
  
  // 获取评委列表
  getList: () => api.get('/judge/list'),
  
  // 创建评委
  create: (data) => api.post('/judge', data),
  
  // 更新评委
  update: (id, data) => api.put(`/judge/${id}`, data),
  
  // 删除评委
  delete: (id) => api.delete(`/judge/${id}`)
}

export const institutionApi = {
  // 获取机构列表
  getList: () => api.get('/institution/list'),
  
  // 创建机构
  create: (data) => api.post('/institution', data),
  
  // 更新机构
  update: (id, data) => api.put(`/institution/${id}`, data),
  
  // 删除机构
  delete: (id) => api.delete(`/institution/${id}`)
}

export const taskApi = {
  // 获取当前任务
  getCurrent: () => api.get('/task/current'),
  
  // 获取待评任务列表
  getPending: (judgeId) => api.get(`/task/pending?judgeId=${judgeId}`),
  
  // 获取任务列表
  getList: () => api.get('/task/list'),
  
  // 创建任务
  create: (data) => api.post('/task', data),
  
  // 更新任务
  update: (id, data) => api.put(`/task/${id}`, data),
  
  // 删除任务
  delete: (id) => api.delete(`/task/${id}`),
  
  // 设置当前任务
  setCurrent: (id) => api.post(`/task/${id}/set-current`)
}

export const scoreApi = {
  // 提交评分
  submit: (data) => api.post('/score/submit', data),
  
  // 获取评分结果
  getResults: (taskId) => api.get(`/score/results/${taskId}`),
  
  // 获取单个机构评分结果
  getResult: (taskId, institutionId) => api.get(`/score/result?taskId=${taskId}&institutionId=${institutionId}`),
  
  // 评分记录管理
  getRecords: (params = {}) => {
    const query = new URLSearchParams(params).toString()
    return api.get(`/score/records${query ? '?' + query : ''}`)
  },
  
  // 获取单条评分详情
  getRecord: (id) => api.get(`/score/record/${id}`),
  
  // 删除评分记录
  deleteRecord: (id) => api.delete(`/score/record/${id}`),
  
  // 批量删除评分记录
  batchDelete: (ids) => api.post('/score/records/batch-delete', { ids }),
  
  // 导出评分记录
  exportRecords: (params = {}) => {
    const query = new URLSearchParams(params).toString()
    return api.get(`/score/export${query ? '?' + query : ''}`)
  },
  
  // 导出Excel
  exportExcel: (params = {}) => {
    const query = new URLSearchParams(params).toString()
    return api.get(`/score/export/excel${query ? '?' + query : ''}`)
  },
  
  // 获取评分统计
  getStatistics: (params = {}) => {
    const query = new URLSearchParams(params).toString()
    return api.get(`/score/statistics${query ? '?' + query : ''}`)
  },
  
  // 获取评委评分统计
  getJudgeStats: (params = {}) => {
    const query = new URLSearchParams(params).toString()
    return api.get(`/score/judge-stats${query ? '?' + query : ''}`)
  },
  
  // 获取机构评分统计
  getInstitutionStats: (params = {}) => {
    const query = new URLSearchParams(params).toString()
    return api.get(`/score/institution-stats${query ? '?' + query : ''}`)
  }
}

export const templateApi = {
  // 获取默认评分表模板
  getDefault: () => api.get('/score-template/default'),
  
  // 获取模板列表
  getList: () => api.get('/score-template/list'),
  
  // 创建模板
  create: (data) => api.post('/score-template', data),
  
  // 更新模板
  update: (id, data) => api.put(`/score-template/${id}`, data),
  
  // 设置默认模板
  setDefault: (id) => api.post(`/score-template/${id}/set-default`)
}

export const bonusApi = {
  // 获取单个附加项
  get: (taskId, institutionId) => api.get(`/bonus?taskId=${taskId}&institutionId=${institutionId}`),
  
  // 获取任务的所有附加项列表
  getList: (taskId) => api.get(`/bonus/list/${taskId}`),
  
  // 设置附加项（创建或更新）
  set: (data) => api.post('/bonus', data),
  
  // 更新附加项
  update: (id, data) => api.put(`/bonus/${id}`, data),
  
  // 批量设置（待后端实现）
  batchSet: (dataList) => api.post('/bonus/batch', dataList)
}

export const systemConfigApi = {
  // 获取系统总分
  getTotalScore: () => api.get('/system-config/total-score'),
  
  // 设置系统总分
  setTotalScore: (score) => api.put(`/system-config/total-score?score=${score}`),
  
  // 获取所有配置
  getList: () => api.get('/system-config/list'),
  
  // 获取指定配置
  get: (key) => api.get(`/system-config/${key}`),
  
  // 更新配置
  updateByKey: (key, value) => api.put(`/system-config/key/${key}?value=${value}`)
}

export default api