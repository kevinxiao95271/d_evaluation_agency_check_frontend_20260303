<template>
  <div class="home-container">
    <!-- 头部 -->
    <div class="header">
      <div class="header-left">
        <h2>机构考核评估系统</h2>
        <span class="task-info" v-if="currentTask">
          当前任务：{{ currentTask.name }} ({{ currentTask.period }})
        </span>
      </div>
      <div class="header-right">
        <el-dropdown @command="handleCommand">
          <span class="user-info">
            <el-icon><User /></el-icon>
            {{ judge.name }} ({{ judgeTypeText }})
          </span>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="logout">退出登录</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </div>

    <!-- 主要内容 -->
    <div class="main-content">
      <div class="content-header">
        <h3>待评机构列表</h3>
        <div class="stats">
          <el-tag type="info">总计：{{ pendingTasks.length }} 个机构</el-tag>
          <el-tag type="success">已评：{{ completedCount }} 个</el-tag>
          <el-tag type="warning">待评：{{ pendingCount }} 个</el-tag>
        </div>
      </div>

      <!-- 机构列表 -->
      <div class="institution-grid" v-loading="loading">
        <div 
          v-for="task in pendingTasks" 
          :key="task.taskInstitutionId"
          class="institution-card"
          :class="{ 'completed': task.hasScored }"
        >
          <div class="card-header">
            <h4>{{ task.institutionName }}</h4>
            <el-tag 
              :type="task.hasScored ? 'success' : 'warning'"
              size="small"
            >
              {{ task.hasScored ? '已评分' : '待评分' }}
            </el-tag>
          </div>
          
          <div class="card-content">
            <p class="institution-type">{{ task.institutionTypeName }}</p>
            <p class="material-desc">{{ task.materialDescription }}</p>
            <p class="date-range">
              评估期间：{{ task.startDate }} 至 {{ task.endDate }}
            </p>
          </div>
          
          <div class="card-actions">
            <el-button 
              v-if="!task.hasScored"
              type="primary" 
              @click="goToScore(task)"
              :icon="Edit"
            >
              去评分
            </el-button>
            <el-button 
              v-else
              type="success" 
              @click="goToScore(task)"
              :icon="View"
            >
              查看评分
            </el-button>
          </div>
        </div>
      </div>

      <!-- 空状态 -->
      <el-empty 
        v-if="!loading && pendingTasks.length === 0"
        description="暂无待评机构"
      />
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { User, Edit, View } from '@element-plus/icons-vue'
import { taskApi } from '../api'

export default {
  name: 'Home',
  components: {
    User,
    Edit,
    View
  },
  setup() {
    const router = useRouter()
    const loading = ref(false)
    const currentTask = ref(null)
    const pendingTasks = ref([])
    
    // 从localStorage获取评委信息
    const judge = JSON.parse(localStorage.getItem('judge') || '{}')
    
    // 评委类型文本
    const judgeTypeText = computed(() => {
      return judge.type === 'EXPERT' ? '专家评委' : '大众评委'
    })
    
    // 统计信息
    const completedCount = computed(() => 
      pendingTasks.value.filter(task => task.hasScored).length
    )
    
    const pendingCount = computed(() => 
      pendingTasks.value.filter(task => !task.hasScored).length
    )
    
    // 获取当前任务
    const getCurrentTask = async () => {
      try {
        const task = await taskApi.getCurrent()
        currentTask.value = task
      } catch (error) {
        console.error('获取当前任务失败:', error)
      }
    }
    
    // 获取待评任务列表
    const getPendingTasks = async () => {
      try {
        loading.value = true
        const tasks = await taskApi.getPending(judge.id)
        pendingTasks.value = tasks
      } catch (error) {
        console.error('获取待评任务失败:', error)
        ElMessage.error('获取待评任务失败')
      } finally {
        loading.value = false
      }
    }
    
    // 去评分
    const goToScore = (task) => {
      router.push(`/score/${task.taskId}/${task.institutionId}`)
    }
    
    // 处理下拉菜单命令
    const handleCommand = async (command) => {
      if (command === 'logout') {
        try {
          await ElMessageBox.confirm('确定要退出登录吗？', '提示', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          })
          
          localStorage.removeItem('judge')
          router.push('/login')
          ElMessage.success('已退出登录')
        } catch {
          // 用户取消
        }
      }
    }
    
    // 初始化
    onMounted(() => {
      getCurrentTask()
      getPendingTasks()
    })
    
    return {
      loading,
      currentTask,
      pendingTasks,
      judge,
      judgeTypeText,
      completedCount,
      pendingCount,
      goToScore,
      handleCommand
    }
  }
}
</script>

<style scoped>
.home-container {
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

.header-left h2 {
  margin: 0;
  color: #333;
  font-size: 20px;
}

.task-info {
  margin-left: 16px;
  color: #666;
  font-size: 14px;
}

.user-info {
  display: flex;
  align-items: center;
  cursor: pointer;
  color: #333;
  font-size: 14px;
}

.user-info .el-icon {
  margin-right: 8px;
}

.main-content {
  padding: 24px;
  max-width: 1200px;
  margin: 0 auto;
}

.content-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.content-header h3 {
  margin: 0;
  color: #333;
}

.stats .el-tag {
  margin-left: 8px;
}

.institution-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 20px;
}

.institution-card {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  border-left: 4px solid #409eff;
}

.institution-card:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
  transform: translateY(-2px);
}

.institution-card.completed {
  border-left-color: #67c23a;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.card-header h4 {
  margin: 0;
  color: #333;
  font-size: 16px;
  font-weight: 600;
}

.card-content {
  margin-bottom: 20px;
}

.card-content p {
  margin: 8px 0;
  color: #666;
  font-size: 14px;
  line-height: 1.5;
}

.institution-type {
  color: #409eff !important;
  font-weight: 500;
}

.material-desc {
  background: #f8f9fa;
  padding: 8px 12px;
  border-radius: 4px;
  border-left: 3px solid #409eff;
}

.date-range {
  font-size: 13px !important;
  color: #999 !important;
}

.card-actions {
  text-align: right;
}
</style>