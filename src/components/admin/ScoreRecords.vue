<template>
  <div class="score-records">
    <div class="header">
      <h3>评分记录管理</h3>
      <div class="header-actions">
        <el-button type="primary" @click="exportRecords" :icon="Download">
          导出记录
        </el-button>
        <el-button @click="refreshData" :icon="Refresh">
          刷新
        </el-button>
      </div>
    </div>

    <!-- 筛选条件 -->
    <div class="filters">
      <el-row :gutter="20">
        <el-col :span="6">
          <el-select
            v-model="filters.taskId"
            placeholder="选择考核任务"
            clearable
            @change="loadRecords"
          >
            <el-option
              v-for="task in tasks"
              :key="task.id"
              :label="task.name"
              :value="task.id"
            />
          </el-select>
        </el-col>
        <el-col :span="6">
          <el-select
            v-model="filters.judgeId"
            placeholder="选择评审专家"
            clearable
            filterable
            @change="loadRecords"
          >
            <el-option
              v-for="judge in judges"
              :key="judge.id"
              :label="`${judge.name} (${judge.type === 'EXPERT' ? '专家' : '大众'})`"
              :value="judge.id"
            />
          </el-select>
        </el-col>
        <el-col :span="6">
          <el-select
            v-model="filters.institutionId"
            placeholder="选择被考核机构"
            clearable
            filterable
            @change="loadRecords"
          >
            <el-option
              v-for="institution in institutions"
              :key="institution.id"
              :label="institution.name"
              :value="institution.id"
            />
          </el-select>
        </el-col>
        <el-col :span="6">
          <el-select
            v-model="filters.scoreMode"
            placeholder="评分模式"
            clearable
            @change="loadRecords"
          >
            <el-option label="直接打总分" value="TOTAL" />
            <el-option label="逐条打分" value="ITEM" />
          </el-select>
        </el-col>
      </el-row>
    </div>

    <!-- 统计信息 -->
    <div class="stats">
      <el-row :gutter="20">
        <el-col :span="6">
          <div class="stat-card">
            <div class="stat-number">{{ totalRecords }}</div>
            <div class="stat-label">总评分记录</div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-card">
            <div class="stat-number">{{ expertRecords }}</div>
            <div class="stat-label">专家评分</div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-card">
            <div class="stat-number">{{ publicRecords }}</div>
            <div class="stat-label">大众评分</div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-card">
            <div class="stat-number">{{ avgScore.toFixed(1) }}</div>
            <div class="stat-label">平均分</div>
          </div>
        </el-col>
      </el-row>
    </div>

    <!-- 评分记录表格 -->
    <el-table
      :data="paginatedRecords"
      v-loading="loading"
      stripe
      border
      style="width: 100%"
      @sort-change="handleSortChange"
    >
      <el-table-column prop="id" label="记录ID" width="80" sortable />
      
      <el-table-column prop="taskName" label="考核任务" width="150" />
      
      <el-table-column prop="judgeName" label="评审专家" width="120">
        <template #default="{ row }">
          <el-tag :type="row.judgeType === 'EXPERT' ? 'danger' : 'primary'" size="small">
            {{ row.judgeType === 'EXPERT' ? '专家' : '大众' }}
          </el-tag>
          {{ row.judgeName }}
        </template>
      </el-table-column>
      
      <el-table-column prop="institutionName" label="被考核机构" width="180" />
      
      <el-table-column prop="scoreMode" label="评分模式" width="100">
        <template #default="{ row }">
          <el-tag :type="row.scoreMode === 'TOTAL' ? 'success' : 'info'" size="small">
            {{ row.scoreMode === 'TOTAL' ? '总分' : '逐条' }}
          </el-tag>
        </template>
      </el-table-column>
      
      <el-table-column prop="totalScore" label="总分" width="80" sortable>
        <template #default="{ row }">
          <span :class="{ 'high-score': row.totalScore >= 40, 'low-score': row.totalScore < 30 }">
            {{ row.totalScore }}
          </span>
        </template>
      </el-table-column>
      
      <el-table-column prop="submitTime" label="提交时间" width="160" sortable>
        <template #default="{ row }">
          {{ formatDateTime(row.submitTime) }}
        </template>
      </el-table-column>
      
      <el-table-column prop="comment" label="评价意见" min-width="200">
        <template #default="{ row }">
          <el-tooltip :content="row.comment" placement="top" :disabled="!row.comment">
            <span class="comment-text">{{ row.comment || '无' }}</span>
          </el-tooltip>
        </template>
      </el-table-column>
      
      <el-table-column label="操作" width="150" fixed="right">
        <template #default="{ row }">
          <el-button type="primary" size="small" @click="viewDetail(row)" :icon="View">
            详情
          </el-button>
          <el-button type="danger" size="small" @click="deleteRecord(row)" :icon="Delete">
            删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 分页 -->
    <div class="pagination">
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :page-sizes="[10, 20, 50, 100]"
        :total="filteredRecords.length"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>

    <!-- 详情对话框 -->
    <el-dialog
      v-model="detailVisible"
      title="评分详情"
      width="800px"
      :before-close="handleDetailClose"
    >
      <div v-if="selectedRecord" class="detail-content">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="记录ID">{{ selectedRecord.id }}</el-descriptions-item>
          <el-descriptions-item label="考核任务">{{ selectedRecord.taskName }}</el-descriptions-item>
          <el-descriptions-item label="评审专家">
            <el-tag :type="selectedRecord.judgeType === 'EXPERT' ? 'danger' : 'primary'" size="small">
              {{ selectedRecord.judgeType === 'EXPERT' ? '专家' : '大众' }}
            </el-tag>
            {{ selectedRecord.judgeName }}
          </el-descriptions-item>
          <el-descriptions-item label="被考核机构">{{ selectedRecord.institutionName }}</el-descriptions-item>
          <el-descriptions-item label="评分模式">
            <el-tag :type="selectedRecord.scoreMode === 'TOTAL' ? 'success' : 'info'" size="small">
              {{ selectedRecord.scoreMode === 'TOTAL' ? '直接打总分' : '逐条打分' }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="总分">
            <span class="score-display">{{ selectedRecord.totalScore }}</span>
          </el-descriptions-item>
          <el-descriptions-item label="提交时间">{{ formatDateTime(selectedRecord.submitTime) }}</el-descriptions-item>
          <el-descriptions-item label="评价意见" :span="2">
            {{ selectedRecord.comment || '无评价意见' }}
          </el-descriptions-item>
        </el-descriptions>

        <!-- 逐条评分详情 -->
        <div v-if="selectedRecord.scoreMode === 'ITEM' && selectedRecord.itemScores" class="item-scores">
          <h4>各条目评分详情</h4>
          <el-table :data="selectedRecord.itemScores" border size="small">
            <el-table-column prop="categoryName" label="评分类别" width="120" />
            <el-table-column prop="itemName" label="评分条目" width="200" />
            <el-table-column prop="maxScore" label="满分" width="80" />
            <el-table-column prop="score" label="得分" width="80">
              <template #default="{ row }">
                <span :class="{ 'high-score': row.score >= row.maxScore * 0.8, 'low-score': row.score < row.maxScore * 0.6 }">
                  {{ row.score }}
                </span>
              </template>
            </el-table-column>
            <el-table-column prop="comment" label="备注" min-width="150">
              <template #default="{ row }">
                {{ row.comment || '无' }}
              </template>
            </el-table-column>
          </el-table>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Download, Refresh, View, Delete } from '@element-plus/icons-vue'
import { scoreApi, taskApi, judgeApi, institutionApi } from '../../api'

export default {
  name: 'ScoreRecords',
  components: { Download, Refresh, View, Delete },
  setup() {
    const loading = ref(false)
    const records = ref([])
    const tasks = ref([])
    const judges = ref([])
    const institutions = ref([])
    
    const filters = ref({
      taskId: null,
      judgeId: null,
      institutionId: null,
      scoreMode: null
    })
    
    const currentPage = ref(1)
    const pageSize = ref(20)
    const sortField = ref('submitTime')
    const sortOrder = ref('desc')
    
    const detailVisible = ref(false)
    const selectedRecord = ref(null)
    
    // 筛选后的记录
    const filteredRecords = computed(() => {
      let result = [...records.value]
      
      if (filters.value.taskId) {
        result = result.filter(r => r.taskId === filters.value.taskId)
      }
      if (filters.value.judgeId) {
        result = result.filter(r => r.judgeId === filters.value.judgeId)
      }
      if (filters.value.institutionId) {
        result = result.filter(r => r.institutionId === filters.value.institutionId)
      }
      if (filters.value.scoreMode) {
        result = result.filter(r => r.scoreMode === filters.value.scoreMode)
      }
      
      // 排序
      result.sort((a, b) => {
        const aVal = a[sortField.value]
        const bVal = b[sortField.value]
        
        if (sortOrder.value === 'asc') {
          return aVal > bVal ? 1 : -1
        } else {
          return aVal < bVal ? 1 : -1
        }
      })
      
      return result
    })
    
    // 分页后的记录
    const paginatedRecords = computed(() => {
      const start = (currentPage.value - 1) * pageSize.value
      const end = start + pageSize.value
      return filteredRecords.value.slice(start, end)
    })
    
    // 统计信息
    const totalRecords = computed(() => filteredRecords.value.length)
    const expertRecords = computed(() => filteredRecords.value.filter(r => r.judgeType === 'EXPERT').length)
    const publicRecords = computed(() => filteredRecords.value.filter(r => r.judgeType === 'PUBLIC').length)
    const avgScore = computed(() => {
      if (filteredRecords.value.length === 0) return 0
      const sum = filteredRecords.value.reduce((acc, r) => acc + r.totalScore, 0)
      return sum / filteredRecords.value.length
    })
    
    // 加载评分记录
    const loadRecords = async () => {
      try {
        loading.value = true
        
        // 构建查询参数
        const params = {}
        if (filters.value.taskId) params.taskId = filters.value.taskId
        if (filters.value.judgeId) params.judgeId = filters.value.judgeId
        if (filters.value.institutionId) params.institutionId = filters.value.institutionId
        if (filters.value.scoreMode) params.scoreMode = filters.value.scoreMode
        
        // 调用真实API
        const data = await scoreApi.getRecords(params)
        records.value = data || []
        
      } catch (error) {
        console.error('加载评分记录失败:', error)
        ElMessage.error('加载评分记录失败')
        // 如果API失败，使用模拟数据作为后备
        records.value = generateMockRecords()
      } finally {
        loading.value = false
      }
    }
    
    // 加载基础数据
    const loadBaseData = async () => {
      try {
        // 加载任务列表
        const currentTask = await taskApi.getCurrent()
        tasks.value = currentTask ? [currentTask] : []
        
        // 加载评委列表
        const judgeList = await judgeApi.getList()
        judges.value = judgeList || []
        
        // 加载机构列表
        const institutionList = await institutionApi.getList()
        institutions.value = institutionList || []
        
        // 设置默认任务
        if (currentTask) {
          filters.value.taskId = currentTask.id
        }
        
      } catch (error) {
        console.error('加载基础数据失败:', error)
        ElMessage.error('加载基础数据失败')
        
        // 使用模拟数据作为后备
        tasks.value = [{ id: 1, name: '2026年第一季度考核' }]
        judges.value = Array.from({ length: 76 }, (_, i) => ({
          id: i + 1,
          name: i < 38 ? `专家${i + 1}` : `大众评委${i - 37}`,
          type: i < 38 ? 'EXPERT' : 'PUBLIC'
        }))
        institutions.value = Array.from({ length: 64 }, (_, i) => ({
          id: i + 1,
          name: `机构${i + 1}`
        }))
      }
    }
    
    // 生成模拟数据
    const generateMockRecords = () => {
      const mockData = []
      const scoreModes = ['TOTAL', 'ITEM']
      
      for (let i = 1; i <= 200; i++) {
        const judgeIndex = Math.floor(Math.random() * 76)
        const institutionIndex = Math.floor(Math.random() * 64)
        const scoreMode = scoreModes[Math.floor(Math.random() * 2)]
        
        mockData.push({
          id: i,
          taskId: 1,
          taskName: '2026年第一季度考核',
          judgeId: judgeIndex + 1,
          judgeName: judgeIndex < 38 ? `专家${judgeIndex + 1}` : `大众评委${judgeIndex - 37}`,
          judgeType: judgeIndex < 38 ? 'EXPERT' : 'PUBLIC',
          institutionId: institutionIndex + 1,
          institutionName: `机构${institutionIndex + 1}`,
          scoreMode,
          totalScore: Math.round((Math.random() * 20 + 25) * 10) / 10, // 25-45分
          submitTime: new Date(Date.now() - Math.random() * 30 * 24 * 60 * 60 * 1000).toISOString(),
          comment: Math.random() > 0.7 ? `评价意见${i}` : null,
          itemScores: scoreMode === 'ITEM' ? generateItemScores() : null
        })
      }
      
      return mockData
    }
    
    // 生成条目评分数据
    const generateItemScores = () => {
      return [
        { categoryName: '基础管理', itemName: '组织建设', maxScore: 10, score: Math.round(Math.random() * 3 + 7), comment: '良好' },
        { categoryName: '基础管理', itemName: '制度建设', maxScore: 8, score: Math.round(Math.random() * 2 + 6), comment: null },
        { categoryName: '业务开展', itemName: '技术水平', maxScore: 15, score: Math.round(Math.random() * 4 + 11), comment: '优秀' },
        { categoryName: '业务开展', itemName: '服务质量', maxScore: 12, score: Math.round(Math.random() * 3 + 9), comment: null }
      ]
    }
    
    // 查看详情
    const viewDetail = (record) => {
      selectedRecord.value = record
      detailVisible.value = true
    }
    
    // 删除记录
    const deleteRecord = async (record) => {
      try {
        await ElMessageBox.confirm(`确定要删除评委"${record.judgeName}"对"${record.institutionName}"的评分记录吗？`, '确认删除', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        })
        
        // 调用真实API删除
        await scoreApi.deleteRecord(record.id)
        
        // 从本地数据中移除
        const index = records.value.findIndex(r => r.id === record.id)
        if (index > -1) {
          records.value.splice(index, 1)
        }
        
        ElMessage.success('删除成功')
        
      } catch (error) {
        if (error !== 'cancel') {
          console.error('删除失败:', error)
          ElMessage.error('删除失败')
        }
      }
    }
    
    // 导出记录
    const exportRecords = async () => {
      try {
        // 构建导出参数
        const params = {}
        if (filters.value.taskId) params.taskId = filters.value.taskId
        if (filters.value.judgeId) params.judgeId = filters.value.judgeId
        if (filters.value.institutionId) params.institutionId = filters.value.institutionId
        
        // 调用导出API
        const result = await scoreApi.exportRecords(params)
        
        // 处理导出结果（这里假设返回CSV内容）
        if (result) {
          const blob = new Blob([result], { type: 'text/csv;charset=utf-8;' })
          const link = document.createElement('a')
          const url = URL.createObjectURL(blob)
          link.setAttribute('href', url)
          link.setAttribute('download', `评分记录_${new Date().toISOString().slice(0, 10)}.csv`)
          link.style.visibility = 'hidden'
          document.body.appendChild(link)
          link.click()
          document.body.removeChild(link)
          
          ElMessage.success('导出成功')
        } else {
          ElMessage.warning('暂无数据可导出')
        }
        
      } catch (error) {
        console.error('导出失败:', error)
        ElMessage.error('导出功能暂时不可用')
      }
    }
    
    // 刷新数据
    const refreshData = () => {
      loadRecords()
      ElMessage.success('数据已刷新')
    }
    
    // 格式化日期时间
    const formatDateTime = (dateStr) => {
      if (!dateStr) return ''
      const date = new Date(dateStr)
      return date.toLocaleString('zh-CN')
    }
    
    // 排序处理
    const handleSortChange = ({ prop, order }) => {
      sortField.value = prop
      sortOrder.value = order === 'ascending' ? 'asc' : 'desc'
    }
    
    // 分页处理
    const handleSizeChange = (size) => {
      pageSize.value = size
      currentPage.value = 1
    }
    
    const handleCurrentChange = (page) => {
      currentPage.value = page
    }
    
    // 关闭详情对话框
    const handleDetailClose = () => {
      detailVisible.value = false
      selectedRecord.value = null
    }
    
    // 初始化
    onMounted(() => {
      loadBaseData()
      loadRecords()
    })
    
    return {
      loading,
      records,
      tasks,
      judges,
      institutions,
      filters,
      currentPage,
      pageSize,
      detailVisible,
      selectedRecord,
      filteredRecords,
      paginatedRecords,
      totalRecords,
      expertRecords,
      publicRecords,
      avgScore,
      loadRecords,
      viewDetail,
      deleteRecord,
      exportRecords,
      refreshData,
      formatDateTime,
      handleSortChange,
      handleSizeChange,
      handleCurrentChange,
      handleDetailClose
    }
  }
}
</script>

<style scoped>
.score-records {
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.header h3 {
  margin: 0;
  color: #333;
}

.header-actions {
  display: flex;
  gap: 10px;
}

.filters {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
}

.stats {
  margin-bottom: 20px;
}

.stat-card {
  background: white;
  padding: 20px;
  border-radius: 8px;
  text-align: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.stat-number {
  font-size: 28px;
  font-weight: bold;
  color: #409eff;
  margin-bottom: 8px;
}

.stat-label {
  color: #666;
  font-size: 14px;
}

.high-score {
  color: #67c23a;
  font-weight: bold;
}

.low-score {
  color: #f56c6c;
  font-weight: bold;
}

.comment-text {
  display: inline-block;
  max-width: 200px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.pagination {
  margin-top: 20px;
  text-align: right;
}

.detail-content {
  max-height: 600px;
  overflow-y: auto;
}

.item-scores {
  margin-top: 20px;
}

.item-scores h4 {
  margin-bottom: 15px;
  color: #333;
}

.score-display {
  font-size: 18px;
  font-weight: bold;
  color: #409eff;
}
</style>