<template>
  <div class="results-statistics">
    <div class="section-header">
      <h3>结果统计</h3>
      <div class="header-actions">
        <el-select v-model="selectedTaskId" placeholder="选择考核任务" @change="loadResults">
          <el-option 
            v-for="task in tasks" 
            :key="task.id" 
            :label="task.name" 
            :value="task.id" 
          />
        </el-select>
        <el-button type="success" @click="exportResults" :icon="Download">
          导出结果
        </el-button>
      </div>
    </div>

    <!-- 统计概览 -->
    <div class="stats-overview" v-if="selectedTaskId">
      <el-row :gutter="20">
        <el-col :span="6">
          <div class="stat-card">
            <div class="stat-number">{{ totalInstitutions }}</div>
            <div class="stat-label">参评机构</div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-card">
            <div class="stat-number">{{ completedInstitutions }}</div>
            <div class="stat-label">已完成评分</div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-card">
            <div class="stat-number">{{ averageScore.toFixed(1) }}</div>
            <div class="stat-label">平均得分</div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-card">
            <div class="stat-number">{{ highestScore.toFixed(1) }}</div>
            <div class="stat-label">最高得分</div>
          </div>
        </el-col>
      </el-row>
    </div>

    <!-- 排名表格 -->
    <div class="ranking-table" v-loading="loading">
      <el-table :data="results" stripe border>
        <el-table-column prop="rank" label="排名" width="80" align="center">
          <template #default="{ row }">
            <el-tag 
              :type="getRankType(row.rank)" 
              :effect="row.rank <= 3 ? 'dark' : 'plain'"
            >
              {{ row.rank }}
            </el-tag>
          </template>
        </el-table-column>
        
        <el-table-column prop="institutionName" label="机构名称" min-width="200" />
        
        <el-table-column label="专家评分" width="120" align="center">
          <template #default="{ row }">
            <div class="score-cell">
              <div class="score-value">{{ row.expertAvgScore?.toFixed(1) || '-' }}</div>
              <div class="score-detail">{{ row.expertJudgeCount || 0 }}人评分</div>
            </div>
          </template>
        </el-table-column>
        
        <el-table-column label="大众评分" width="120" align="center">
          <template #default="{ row }">
            <div class="score-cell">
              <div class="score-value">{{ row.publicAvgScore?.toFixed(1) || '-' }}</div>
              <div class="score-detail">{{ row.publicJudgeCount || 0 }}人评分</div>
            </div>
          </template>
        </el-table-column>
        
        <el-table-column label="专家贡献分" width="120" align="center">
          <template #default="{ row }">
            {{ row.expertContribution?.toFixed(2) || '-' }}
          </template>
        </el-table-column>
        
        <el-table-column label="大众贡献分" width="120" align="center">
          <template #default="{ row }">
            {{ row.publicContribution?.toFixed(2) || '-' }}
          </template>
        </el-table-column>
        
        <el-table-column label="附加分" width="100" align="center">
          <template #default="{ row }">
            <div class="bonus-cell">
              <div>{{ (row.directorBonus || 0) + (row.secretaryBonus || 0) }}</div>
              <div class="bonus-detail">
                <span v-if="row.directorBonus">主任+{{ row.directorBonus }}</span>
                <span v-if="row.secretaryBonus">秘书+{{ row.secretaryBonus }}</span>
              </div>
            </div>
          </template>
        </el-table-column>
        
        <el-table-column prop="finalScore" label="最终得分" width="120" align="center">
          <template #default="{ row }">
            <div class="final-score">{{ row.finalScore?.toFixed(2) || '-' }}</div>
          </template>
        </el-table-column>
        
        <el-table-column label="操作" width="150" fixed="right">
          <template #default="{ row }">
            <el-button size="small" @click="viewDetail(row)" :icon="View">
              查看详情
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <!-- 详情对话框 -->
    <el-dialog 
      title="评分详情" 
      v-model="detailVisible" 
      width="800px"
    >
      <div v-if="selectedResult">
        <h4>{{ selectedResult.institutionName }} - 评分详情</h4>
        
        <!-- 总体得分 -->
        <div class="detail-summary">
          <el-descriptions :column="2" border>
            <el-descriptions-item label="最终排名">
              <el-tag :type="getRankType(selectedResult.rank)">
                第 {{ selectedResult.rank }} 名
              </el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="最终得分">
              {{ selectedResult.finalScore?.toFixed(2) }} 分
            </el-descriptions-item>
            <el-descriptions-item label="专家平均分">
              {{ selectedResult.expertAvgScore?.toFixed(1) }} 分 ({{ selectedResult.expertJudgeCount }}人)
            </el-descriptions-item>
            <el-descriptions-item label="大众平均分">
              {{ selectedResult.publicAvgScore?.toFixed(1) }} 分 ({{ selectedResult.publicJudgeCount }}人)
            </el-descriptions-item>
            <el-descriptions-item label="专家贡献分">
              {{ selectedResult.expertContribution?.toFixed(2) }} 分 (70%)
            </el-descriptions-item>
            <el-descriptions-item label="大众贡献分">
              {{ selectedResult.publicContribution?.toFixed(2) }} 分 (20%)
            </el-descriptions-item>
            <el-descriptions-item label="主任演讲加分">
              {{ selectedResult.directorBonus || 0 }} 分
            </el-descriptions-item>
            <el-descriptions-item label="秘书参与加分">
              {{ selectedResult.secretaryBonus || 0 }} 分
            </el-descriptions-item>
          </el-descriptions>
        </div>
        
        <!-- 各条目得分 -->
        <div class="detail-items" v-if="selectedResult.itemResults">
          <h5>各条目得分详情</h5>
          <el-table :data="selectedResult.itemResults" border size="small">
            <el-table-column prop="categoryName" label="分类" width="120" />
            <el-table-column prop="itemName" label="评分条目" min-width="150" />
            <el-table-column prop="expertAvgScore" label="专家平均分" width="120" align="center" />
            <el-table-column prop="publicAvgScore" label="大众平均分" width="120" align="center" />
            <el-table-column prop="finalScore" label="最终得分" width="120" align="center" />
          </el-table>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Download, View } from '@element-plus/icons-vue'
import { taskApi, scoreApi } from '../../api'

export default {
  name: 'ResultsStatistics',
  components: {
    Download,
    View
  },
  setup() {
    const loading = ref(false)
    const detailVisible = ref(false)
    const selectedTaskId = ref(null)
    const selectedResult = ref(null)
    
    const tasks = ref([])
    const results = ref([])
    
    // 计算统计数据
    const totalInstitutions = computed(() => results.value.length)
    
    const completedInstitutions = computed(() => 
      results.value.filter(r => r.finalScore !== null && r.finalScore !== undefined).length
    )
    
    const averageScore = computed(() => {
      const validScores = results.value
        .filter(r => r.finalScore !== null && r.finalScore !== undefined)
        .map(r => r.finalScore)
      
      return validScores.length > 0 
        ? validScores.reduce((sum, score) => sum + score, 0) / validScores.length 
        : 0
    })
    
    const highestScore = computed(() => {
      const validScores = results.value
        .filter(r => r.finalScore !== null && r.finalScore !== undefined)
        .map(r => r.finalScore)
      
      return validScores.length > 0 ? Math.max(...validScores) : 0
    })
    
    // 获取排名类型
    const getRankType = (rank) => {
      if (rank === 1) return 'danger'  // 金色
      if (rank === 2) return 'warning' // 银色
      if (rank === 3) return 'success' // 铜色
      return 'info'
    }
    
    // 加载任务列表
    const loadTasks = async () => {
      try {
        const data = await taskApi.getList()
        tasks.value = data || []
        
        // 默认选择第一个任务
        if (tasks.value.length > 0) {
          selectedTaskId.value = tasks.value[0].id
          loadResults()
        }
      } catch (error) {
        console.error('加载任务列表失败:', error)
        ElMessage.error('加载任务列表失败')
      }
    }
    
    // 加载结果数据
    const loadResults = async () => {
      if (!selectedTaskId.value) return
      
      try {
        loading.value = true
        const data = await scoreApi.getResults(selectedTaskId.value)
        results.value = data || []
      } catch (error) {
        console.error('加载结果数据失败:', error)
        ElMessage.error('加载结果数据失败')
      } finally {
        loading.value = false
      }
    }
    
    // 查看详情
    const viewDetail = (row) => {
      selectedResult.value = row
      detailVisible.value = true
    }
    
    // 导出结果
    const exportResults = () => {
      if (!selectedTaskId.value || results.value.length === 0) {
        ElMessage.warning('暂无数据可导出')
        return
      }
      
      // 这里实现导出逻辑
      ElMessage.success('导出功能开发中...')
    }
    
    // 初始化
    onMounted(() => {
      loadTasks()
    })
    
    return {
      loading,
      detailVisible,
      selectedTaskId,
      selectedResult,
      tasks,
      results,
      totalInstitutions,
      completedInstitutions,
      averageScore,
      highestScore,
      getRankType,
      loadResults,
      viewDetail,
      exportResults
    }
  }
}
</script>

<style scoped>
.results-statistics {
  height: 100%;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.section-header h3 {
  margin: 0;
  color: #333;
}

.header-actions {
  display: flex;
  gap: 12px;
  align-items: center;
}

.stats-overview {
  margin-bottom: 24px;
}

.stat-card {
  background: white;
  padding: 20px;
  border-radius: 8px;
  text-align: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  border-left: 4px solid #409eff;
}

.stat-number {
  font-size: 32px;
  font-weight: bold;
  color: #409eff;
  margin-bottom: 8px;
}

.stat-label {
  color: #666;
  font-size: 14px;
}

.ranking-table {
  background: white;
  border-radius: 8px;
  overflow: hidden;
}

.score-cell {
  text-align: center;
}

.score-value {
  font-weight: bold;
  color: #333;
}

.score-detail {
  font-size: 12px;
  color: #999;
  margin-top: 2px;
}

.bonus-cell {
  text-align: center;
}

.bonus-detail {
  font-size: 12px;
  color: #999;
  margin-top: 2px;
}

.bonus-detail span {
  display: block;
}

.final-score {
  font-size: 16px;
  font-weight: bold;
  color: #e6a23c;
}

.detail-summary {
  margin-bottom: 24px;
}

.detail-items h5 {
  margin: 20px 0 12px 0;
  color: #333;
}
</style>