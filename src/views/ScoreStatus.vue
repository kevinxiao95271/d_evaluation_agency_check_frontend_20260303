<template>
  <div class="score-status-container">
    <!-- 头部 -->
    <div class="header">
      <div class="header-left">
        <h2>评分状态总览</h2>
      </div>
      <div class="header-right">
        <el-button @click="refreshData" :icon="Refresh" :loading="loading">
          刷新数据
        </el-button>
        <el-button @click="goToLogin" :icon="User">
          切换账号
        </el-button>
      </div>
    </div>

    <!-- 统计卡片 -->
    <div class="stats-cards">
      <el-row :gutter="20">
        <el-col :span="6">
          <div class="stat-card">
            <div class="stat-icon expert">👨‍🎓</div>
            <div class="stat-content">
              <div class="stat-number">{{ expertStats.total }}</div>
              <div class="stat-label">专家评委</div>
              <div class="stat-detail">已评分: {{ expertStats.completed }}</div>
            </div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-card">
            <div class="stat-icon public">👥</div>
            <div class="stat-content">
              <div class="stat-number">{{ publicStats.total }}</div>
              <div class="stat-label">大众评委</div>
              <div class="stat-detail">已评分: {{ publicStats.completed }}</div>
            </div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-card">
            <div class="stat-icon institution">🏢</div>
            <div class="stat-content">
              <div class="stat-number">{{ institutionStats.total }}</div>
              <div class="stat-label">参评机构</div>
              <div class="stat-detail">已完成: {{ institutionStats.completed }}</div>
            </div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-card">
            <div class="stat-icon progress">📊</div>
            <div class="stat-content">
              <div class="stat-number">{{ overallProgress }}%</div>
              <div class="stat-label">总体进度</div>
              <div class="stat-detail">评分完成度</div>
            </div>
          </div>
        </el-col>
      </el-row>
    </div>

    <!-- 机构评分进度 -->
    <div class="progress-section">
      <h3>各机构评分进度</h3>
      <div class="institution-progress" v-loading="loading">
        <div 
          v-for="inst in institutionProgress" 
          :key="inst.id"
          class="progress-item"
        >
          <div class="progress-header">
            <span class="institution-name">{{ inst.name }}</span>
            <span class="progress-text">
              {{ inst.expertCount + inst.publicCount }} / {{ inst.totalRequired }} 
              ({{ Math.round((inst.expertCount + inst.publicCount) / inst.totalRequired * 100) }}%)
            </span>
          </div>
          <div class="progress-bars">
            <div class="progress-bar expert">
              <div class="progress-label">专家评委</div>
              <el-progress 
                :percentage="Math.round(inst.expertCount / inst.expertRequired * 100)"
                :color="getProgressColor(inst.expertCount / inst.expertRequired)"
                :show-text="false"
              />
              <span class="progress-count">{{ inst.expertCount }} / {{ inst.expertRequired }}</span>
            </div>
            <div class="progress-bar public">
              <div class="progress-label">大众评委</div>
              <el-progress 
                :percentage="Math.round(inst.publicCount / inst.publicRequired * 100)"
                :color="getProgressColor(inst.publicCount / inst.publicRequired)"
                :show-text="false"
              />
              <span class="progress-count">{{ inst.publicCount }} / {{ inst.publicRequired }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 评委账号快速测试 -->
    <div class="quick-test-section">
      <h3>评委账号快速测试</h3>
      <div class="test-accounts">
        <div class="account-group">
          <h4>专家评委账号</h4>
          <div class="account-list">
            <div 
              v-for="account in expertAccounts.slice(0, 8)" 
              :key="account.username"
              class="account-item"
              @click="quickLogin(account)"
            >
              <div class="account-info">
                <div class="account-name">{{ account.username }}</div>
                <div class="account-detail">{{ account.name }}</div>
                <div class="account-institution">{{ account.institutionName }}</div>
              </div>
              <div class="account-status" :class="account.status">
                {{ account.statusText }}
              </div>
            </div>
          </div>
        </div>
        
        <div class="account-group">
          <h4>大众评委账号</h4>
          <div class="account-list">
            <div 
              v-for="account in publicAccounts.slice(0, 8)" 
              :key="account.username"
              class="account-item"
              @click="quickLogin(account)"
            >
              <div class="account-info">
                <div class="account-name">{{ account.username }}</div>
                <div class="account-detail">{{ account.name }}</div>
                <div class="account-institution">{{ account.institutionName }}</div>
              </div>
              <div class="account-status" :class="account.status">
                {{ account.statusText }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Refresh, User } from '@element-plus/icons-vue'
import { judgeApi, taskApi, institutionApi } from '../api'

export default {
  name: 'ScoreStatus',
  components: {
    Refresh,
    User
  },
  setup() {
    const router = useRouter()
    const loading = ref(false)
    
    const judges = ref([])
    const institutions = ref([])
    const scoreProgress = ref({})
    
    // 计算统计数据
    const expertStats = computed(() => {
      const experts = judges.value.filter(j => j.type === 'EXPERT')
      return {
        total: experts.length,
        completed: experts.filter(j => j.hasScored).length
      }
    })
    
    const publicStats = computed(() => {
      const publics = judges.value.filter(j => j.type === 'PUBLIC')
      return {
        total: publics.length,
        completed: publics.filter(j => j.hasScored).length
      }
    })
    
    const institutionStats = computed(() => {
      return {
        total: institutions.value.length,
        completed: institutions.value.filter(i => i.isCompleted).length
      }
    })
    
    const overallProgress = computed(() => {
      const totalRequired = judges.value.length * (institutions.value.length - 1) // 减去自己机构
      const totalCompleted = Object.values(scoreProgress.value).reduce((sum, inst) => {
        return sum + (inst.expertCount || 0) + (inst.publicCount || 0)
      }, 0)
      
      return totalRequired > 0 ? Math.round(totalCompleted / totalRequired * 100) : 0
    })
    
    const institutionProgress = computed(() => {
      return institutions.value.map(inst => {
        const progress = scoreProgress.value[inst.id] || {}
        const expertRequired = expertStats.value.total - 1 // 减去自己机构的专家
        const publicRequired = publicStats.value.total - 1 // 减去自己机构的大众
        
        return {
          ...inst,
          expertCount: progress.expertCount || 0,
          publicCount: progress.publicCount || 0,
          expertRequired,
          publicRequired,
          totalRequired: expertRequired + publicRequired
        }
      })
    })
    
    const expertAccounts = computed(() => {
      return judges.value
        .filter(j => j.type === 'EXPERT')
        .map(j => ({
          ...j,
          status: j.hasScored ? 'completed' : 'pending',
          statusText: j.hasScored ? '已评分' : '待评分'
        }))
    })
    
    const publicAccounts = computed(() => {
      return judges.value
        .filter(j => j.type === 'PUBLIC')
        .map(j => ({
          ...j,
          status: j.hasScored ? 'completed' : 'pending',
          statusText: j.hasScored ? '已评分' : '待评分'
        }))
    })
    
    // 获取进度条颜色
    const getProgressColor = (ratio) => {
      if (ratio >= 0.8) return '#67c23a'
      if (ratio >= 0.5) return '#e6a23c'
      return '#f56c6c'
    }
    
    // 加载数据
    const loadData = async () => {
      try {
        loading.value = true
        
        // 并行加载数据
        const [judgesResult, institutionsResult] = await Promise.all([
          judgeApi.getList(),
          institutionApi.getList()
        ])
        
        judges.value = judgesResult
        institutions.value = institutionsResult
        
        // 模拟评分进度数据
        scoreProgress.value = {}
        institutions.value.forEach(inst => {
          scoreProgress.value[inst.id] = {
            expertCount: Math.floor(Math.random() * expertStats.value.total),
            publicCount: Math.floor(Math.random() * publicStats.value.total)
          }
        })
        
        // 模拟评委评分状态
        judges.value.forEach(judge => {
          judge.hasScored = Math.random() > 0.3 // 70%的评委已经评分
        })
        
      } catch (error) {
        console.error('加载数据失败:', error)
        ElMessage.error('加载数据失败')
      } finally {
        loading.value = false
      }
    }
    
    // 刷新数据
    const refreshData = () => {
      loadData()
    }
    
    // 快速登录
    const quickLogin = (account) => {
      // 保存账号信息到localStorage
      localStorage.setItem('judge', JSON.stringify(account))
      ElMessage.success(`已切换到 ${account.name} 账号`)
      router.push('/home')
    }
    
    // 去登录页
    const goToLogin = () => {
      router.push('/login')
    }
    
    // 初始化
    onMounted(() => {
      loadData()
    })
    
    return {
      loading,
      expertStats,
      publicStats,
      institutionStats,
      overallProgress,
      institutionProgress,
      expertAccounts,
      publicAccounts,
      getProgressColor,
      refreshData,
      quickLogin,
      goToLogin
    }
  }
}
</script>

<style scoped>
.score-status-container {
  min-height: 100vh;
  background-color: #f5f5f5;
}

.header {
  background: white;
  padding: 0 24px;
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 100;
}

.header h2 {
  margin: 0;
  color: #333;
  font-size: 20px;
}

.stats-cards {
  padding: 24px;
}

.stat-card {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
}

.stat-icon {
  font-size: 32px;
  margin-right: 16px;
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
}

.stat-icon.expert { background: #e6f7ff; }
.stat-icon.public { background: #f6ffed; }
.stat-icon.institution { background: #fff7e6; }
.stat-icon.progress { background: #f9f0ff; }

.stat-number {
  font-size: 24px;
  font-weight: bold;
  color: #333;
}

.stat-label {
  color: #666;
  font-size: 14px;
  margin: 4px 0;
}

.stat-detail {
  color: #999;
  font-size: 12px;
}

.progress-section {
  padding: 0 24px 24px;
}

.progress-section h3 {
  margin: 0 0 16px 0;
  color: #333;
}

.institution-progress {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.progress-item {
  margin-bottom: 20px;
  padding-bottom: 16px;
  border-bottom: 1px solid #f0f0f0;
}

.progress-item:last-child {
  border-bottom: none;
  margin-bottom: 0;
}

.progress-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.institution-name {
  font-weight: bold;
  color: #333;
}

.progress-text {
  color: #666;
  font-size: 14px;
}

.progress-bars {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.progress-bar {
  display: flex;
  align-items: center;
  gap: 12px;
}

.progress-label {
  width: 80px;
  font-size: 14px;
  color: #666;
}

.progress-count {
  width: 60px;
  text-align: right;
  font-size: 12px;
  color: #999;
}

.quick-test-section {
  padding: 0 24px 24px;
}

.quick-test-section h3 {
  margin: 0 0 16px 0;
  color: #333;
}

.test-accounts {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
}

.account-group h4 {
  margin: 0 0 12px 0;
  color: #333;
  font-size: 16px;
}

.account-list {
  background: white;
  border-radius: 8px;
  padding: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.account-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-bottom: 8px;
}

.account-item:hover {
  background: #f8f9fa;
}

.account-item:last-child {
  margin-bottom: 0;
}

.account-name {
  font-weight: bold;
  color: #333;
  font-family: monospace;
}

.account-detail {
  color: #666;
  font-size: 14px;
  margin: 2px 0;
}

.account-institution {
  color: #999;
  font-size: 12px;
}

.account-status {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
}

.account-status.completed {
  background: #f0f9ff;
  color: #1890ff;
}

.account-status.pending {
  background: #fff7e6;
  color: #fa8c16;
}
</style>