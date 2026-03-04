<template>
  <div class="admin-container">
    <!-- 头部导航 -->
    <div class="admin-header">
      <div class="header-left">
        <h2>管理后台</h2>
      </div>
      <div class="header-right">
        <el-dropdown @command="handleCommand">
          <span class="user-info">
            <el-icon><User /></el-icon>
            管理员
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
    <div class="admin-main">
      <!-- 侧边栏 -->
      <div class="admin-sidebar">
        <el-menu
          :default-active="activeMenu"
          class="sidebar-menu"
          @select="handleMenuSelect"
        >
          <el-menu-item index="institutions">
            <el-icon><HomeFilled /></el-icon>
            <span>机构管理</span>
          </el-menu-item>
          <el-menu-item index="judges">
            <el-icon><UserFilled /></el-icon>
            <span>评委管理</span>
          </el-menu-item>
          <el-menu-item index="tasks">
            <el-icon><Document /></el-icon>
            <span>任务管理</span>
          </el-menu-item>
          <el-menu-item index="templates">
            <el-icon><Edit /></el-icon>
            <span>评分表配置</span>
          </el-menu-item>
          <el-menu-item index="bonus">
            <el-icon><Plus /></el-icon>
            <span>附加项管理</span>
          </el-menu-item>
          <el-menu-item index="config">
            <el-icon><Setting /></el-icon>
            <span>系统配置</span>
          </el-menu-item>
          <el-menu-item index="results">
            <el-icon><DataAnalysis /></el-icon>
            <span>结果统计</span>
          </el-menu-item>
          
          <el-menu-item index="records">
            <el-icon><Document /></el-icon>
            <span>评分记录</span>
          </el-menu-item>
        </el-menu>
      </div>

      <!-- 内容区域 -->
      <div class="admin-content">
        <!-- 机构管理 -->
        <div v-if="activeMenu === 'institutions'" class="content-section">
          <InstitutionManagement />
        </div>

        <!-- 评委管理 -->
        <div v-if="activeMenu === 'judges'" class="content-section">
          <JudgeManagement />
        </div>

        <!-- 任务管理 -->
        <div v-if="activeMenu === 'tasks'" class="content-section">
          <TaskManagement />
        </div>

        <!-- 评分表配置 -->
        <div v-if="activeMenu === 'templates'" class="content-section">
          <TemplateManagement />
        </div>

        <!-- 附加项管理 -->
        <div v-if="activeMenu === 'bonus'" class="content-section">
          <BonusManagement />
        </div>

        <!-- 系统配置 -->
        <div v-if="activeMenu === 'config'" class="content-section">
          <SystemConfig />
        </div>

        <!-- 结果统计 -->
        <div v-if="activeMenu === 'results'" class="content-section">
          <ResultsStatistics />
        </div>
        
        <!-- 评分记录 -->
        <div v-if="activeMenu === 'records'" class="content-section">
          <ScoreRecords />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessageBox, ElMessage } from 'element-plus'
import { 
  User, HomeFilled, UserFilled, Document, Edit, 
  Plus, Setting, DataAnalysis 
} from '@element-plus/icons-vue'

// 导入子组件
import InstitutionManagement from '../components/admin/InstitutionManagement.vue'
import JudgeManagement from '../components/admin/JudgeManagement.vue'
import TaskManagement from '../components/admin/TaskManagement.vue'
import TemplateManagement from '../components/admin/TemplateManagement.vue'
import BonusManagement from '../components/admin/BonusManagement.vue'
import SystemConfig from '../components/admin/SystemConfig.vue'
import ResultsStatistics from '../components/admin/ResultsStatistics.vue'
import ScoreRecords from '../components/admin/ScoreRecords.vue'

export default {
  name: 'Admin',
  components: {
    User,
    HomeFilled,
    UserFilled,
    Document,
    Edit,
    Plus,
    Setting,
    DataAnalysis,
    InstitutionManagement,
    JudgeManagement,
    TaskManagement,
    TemplateManagement,
    BonusManagement,
    SystemConfig,
    ResultsStatistics,
    ScoreRecords
  },
  setup() {
    const router = useRouter()
    const activeMenu = ref('institutions')
    
    const handleMenuSelect = (index) => {
      activeMenu.value = index
    }
    
    const handleCommand = async (command) => {
      if (command === 'logout') {
        try {
          await ElMessageBox.confirm('确定要退出登录吗？', '提示', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          })
          
          localStorage.removeItem('admin')
          router.push('/login')
          ElMessage.success('已退出登录')
        } catch {
          // 用户取消
        }
      }
    }
    
    return {
      activeMenu,
      handleMenuSelect,
      handleCommand
    }
  }
}
</script>

<style scoped>
.admin-container {
  min-height: 100vh;
  background-color: #f5f5f5;
}

.admin-header {
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

.admin-header h2 {
  margin: 0;
  color: #333;
  font-size: 20px;
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

.admin-main {
  display: flex;
  min-height: calc(100vh - 64px);
}

.admin-sidebar {
  width: 240px;
  background: white;
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.1);
}

.sidebar-menu {
  border-right: none;
  height: 100%;
}

.sidebar-menu .el-menu-item {
  height: 56px;
  line-height: 56px;
}

.admin-content {
  flex: 1;
  padding: 24px;
  overflow-y: auto;
}

.content-section {
  background: white;
  border-radius: 8px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}
</style>