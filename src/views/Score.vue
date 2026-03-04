<template>
  <div class="score-container">
    <!-- 头部 -->
    <div class="header">
      <div class="header-left">
        <el-button @click="goBack" :icon="ArrowLeft">返回</el-button>
        <div class="title-info">
          <h2>{{ institutionInfo.name }}</h2>
          <span class="subtitle">{{ currentTask?.name }} - 评分</span>
        </div>
      </div>
      <div class="header-right">
        <span class="judge-info">评委：{{ judge.name }}</span>
      </div>
    </div>

    <!-- 主要内容 -->
    <div class="main-content" v-loading="loading">
      <div class="score-form-container">
        <!-- 评分模式选择 -->
        <div class="mode-selector">
          <h3>评分模式</h3>
          <el-radio-group v-model="scoreMode" @change="onModeChange">
            <el-radio-button label="TOTAL">直接打总分</el-radio-button>
            <el-radio-button label="ITEM">逐条打分</el-radio-button>
          </el-radio-group>
        </div>

        <!-- 直接打总分模式 -->
        <div v-if="scoreMode === 'TOTAL'" class="total-score-mode">
          <div class="score-input-section">
            <h4>总分评定</h4>
            <div class="score-input-wrapper">
              <el-input-number
                v-model="totalScore"
                :min="0"
                :max="templateMaxScore"
                :precision="1"
                :step="0.5"
                size="large"
                class="score-input"
              />
              <span class="score-unit">/ {{ templateMaxScore }} 分</span>
            </div>
            <p class="score-tip">
              系统将根据各条目权重自动分配分数
            </p>
          </div>
        </div>

        <!-- 逐条打分模式 -->
        <div v-if="scoreMode === 'ITEM'" class="item-score-mode">
          <div 
            v-for="category in scoreTemplate?.categories || []" 
            :key="category.id"
            class="category-section"
          >
            <h4 class="category-title">{{ category.name }}</h4>
            <div class="items-list">
              <div 
                v-for="item in category.items" 
                :key="item.id"
                class="score-item"
              >
                <div class="item-info">
                  <h5>{{ item.name }}</h5>
                  <p class="item-desc">{{ item.description }}</p>
                  <span class="item-weight">权重：{{ (item.weight * 100).toFixed(0) }}%</span>
                </div>
                <div class="item-score">
                  <el-input-number
                    v-model="itemScores[item.id]"
                    :min="0"
                    :max="item.maxScore"
                    :precision="1"
                    :step="0.5"
                    size="default"
                  />
                  <span class="max-score">/ {{ item.maxScore }} 分</span>
                </div>
                <div class="item-comment">
                  <el-input
                    v-model="itemComments[item.id]"
                    placeholder="评价意见（可选）"
                    maxlength="200"
                    show-word-limit
                  />
                </div>
              </div>
            </div>
          </div>
          
          <!-- 总分显示 -->
          <div class="calculated-total">
            <h4>计算总分：{{ calculatedTotal.toFixed(1) }} / {{ templateMaxScore }} 分</h4>
          </div>
        </div>

        <!-- 提交按钮 -->
        <div class="submit-section">
          <el-button 
            type="primary" 
            size="large"
            :loading="submitting"
            @click="submitScore"
            :disabled="!canSubmit"
          >
            {{ submitting ? '提交中...' : '提交评分' }}
          </el-button>
          <el-button size="large" @click="goBack">取消</el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { ArrowLeft } from '@element-plus/icons-vue'
import { taskApi, templateApi, scoreApi, institutionApi } from '../api'

export default {
  name: 'Score',
  components: {
    ArrowLeft
  },
  setup() {
    const route = useRoute()
    const router = useRouter()
    
    const loading = ref(false)
    const submitting = ref(false)
    const scoreMode = ref('TOTAL')
    const totalScore = ref(0)
    const itemScores = ref({})
    const itemComments = ref({})
    
    const currentTask = ref(null)
    const scoreTemplate = ref(null)
    const institutionInfo = ref({})
    const templateMaxScore = ref(100)
    
    // 从localStorage获取评委信息
    const judge = JSON.parse(localStorage.getItem('judge') || '{}')
    
    // 路由参数
    const taskId = route.params.taskId
    const institutionId = route.params.institutionId
    
    // 计算总分（逐条打分模式）
    const calculatedTotal = computed(() => {
      if (!scoreTemplate.value?.categories) return 0
      
      let total = 0
      scoreTemplate.value.categories.forEach(category => {
        category.items.forEach(item => {
          const score = itemScores.value[item.id] || 0
          total += score
        })
      })
      return total
    })
    
    // 是否可以提交
    const canSubmit = computed(() => {
      if (scoreMode.value === 'TOTAL') {
        return totalScore.value > 0 && totalScore.value <= templateMaxScore.value
      } else {
        // 逐条打分模式，检查是否所有条目都有分数
        if (!scoreTemplate.value?.categories) return false
        
        for (const category of scoreTemplate.value.categories) {
          for (const item of category.items) {
            if (!itemScores.value[item.id] && itemScores.value[item.id] !== 0) {
              return false
            }
          }
        }
        return true
      }
    })
    
    // 获取当前任务
    const getCurrentTask = async () => {
      try {
        const task = await taskApi.getCurrent()
        currentTask.value = task
      } catch (error) {
        console.error('获取当前任务失败:', error)
      }
    }
    
    // 获取评分表模板
    const getScoreTemplate = async () => {
      try {
        const template = await templateApi.getDefault()
        scoreTemplate.value = template
        templateMaxScore.value = template.templateMaxScore
        
        // 初始化条目分数
        if (template.categories) {
          template.categories.forEach(category => {
            category.items.forEach(item => {
              itemScores.value[item.id] = 0
              itemComments.value[item.id] = ''
            })
          })
        }
      } catch (error) {
        console.error('获取评分表模板失败:', error)
        ElMessage.error('获取评分表模板失败')
      }
    }
    
    // 获取机构信息
    const getInstitutionInfo = async () => {
      try {
        const institutions = await institutionApi.getList()
        const institution = institutions.find(inst => inst.id == institutionId)
        if (institution) {
          institutionInfo.value = institution
        }
      } catch (error) {
        console.error('获取机构信息失败:', error)
      }
    }
    
    // 模式切换
    const onModeChange = () => {
      // 重置数据
      totalScore.value = 0
      Object.keys(itemScores.value).forEach(key => {
        itemScores.value[key] = 0
        itemComments.value[key] = ''
      })
    }
    
    // 提交评分
    const submitScore = async () => {
      try {
        await ElMessageBox.confirm('确定要提交评分吗？提交后不可修改。', '确认提交', {
          confirmButtonText: '确定提交',
          cancelButtonText: '取消',
          type: 'warning'
        })
        
        submitting.value = true
        
        let submitData = {
          taskId: parseInt(taskId),
          institutionId: parseInt(institutionId),
          judgeId: judge.id,
          scoreMode: scoreMode.value
        }
        
        if (scoreMode.value === 'TOTAL') {
          submitData.totalScore = totalScore.value
        } else {
          submitData.itemScores = Object.keys(itemScores.value).map(itemId => ({
            itemId: parseInt(itemId),
            score: itemScores.value[itemId],
            comment: itemComments.value[itemId] || ''
          }))
        }
        
        await scoreApi.submit(submitData)
        
        ElMessage.success('评分提交成功')
        router.push('/home')
        
      } catch (error) {
        if (error.message !== 'cancel') {
          console.error('提交评分失败:', error)
        }
      } finally {
        submitting.value = false
      }
    }
    
    // 返回
    const goBack = () => {
      router.push('/home')
    }
    
    // 初始化
    onMounted(async () => {
      loading.value = true
      try {
        await Promise.all([
          getCurrentTask(),
          getScoreTemplate(),
          getInstitutionInfo()
        ])
      } finally {
        loading.value = false
      }
    })
    
    return {
      loading,
      submitting,
      scoreMode,
      totalScore,
      itemScores,
      itemComments,
      currentTask,
      scoreTemplate,
      institutionInfo,
      templateMaxScore,
      judge,
      calculatedTotal,
      canSubmit,
      onModeChange,
      submitScore,
      goBack
    }
  }
}
</script>

<style scoped>
.score-container {
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

.header-left {
  display: flex;
  align-items: center;
}

.title-info {
  margin-left: 16px;
}

.title-info h2 {
  margin: 0;
  color: #333;
  font-size: 18px;
}

.subtitle {
  color: #666;
  font-size: 14px;
}

.judge-info {
  color: #666;
  font-size: 14px;
}

.main-content {
  padding: 24px;
  max-width: 800px;
  margin: 0 auto;
}

.score-form-container {
  background: white;
  border-radius: 8px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.mode-selector {
  margin-bottom: 32px;
  padding-bottom: 20px;
  border-bottom: 1px solid #eee;
}

.mode-selector h3 {
  margin: 0 0 16px 0;
  color: #333;
}

.total-score-mode {
  margin-bottom: 32px;
}

.score-input-section h4 {
  margin: 0 0 16px 0;
  color: #333;
}

.score-input-wrapper {
  display: flex;
  align-items: center;
  margin-bottom: 12px;
}

.score-input {
  width: 200px;
  margin-right: 12px;
}

.score-unit {
  color: #666;
  font-size: 16px;
}

.score-tip {
  color: #999;
  font-size: 14px;
  margin: 0;
}

.category-section {
  margin-bottom: 32px;
}

.category-title {
  margin: 0 0 16px 0;
  color: #333;
  padding: 8px 12px;
  background: #f8f9fa;
  border-left: 4px solid #409eff;
}

.items-list {
  margin-left: 16px;
}

.score-item {
  display: grid;
  grid-template-columns: 1fr 200px;
  grid-template-rows: auto auto;
  gap: 12px;
  padding: 16px;
  border: 1px solid #eee;
  border-radius: 6px;
  margin-bottom: 16px;
}

.item-info h5 {
  margin: 0 0 8px 0;
  color: #333;
  font-size: 16px;
}

.item-desc {
  margin: 0 0 8px 0;
  color: #666;
  font-size: 14px;
  line-height: 1.5;
}

.item-weight {
  color: #409eff;
  font-size: 12px;
}

.item-score {
  display: flex;
  align-items: center;
  justify-self: end;
}

.max-score {
  margin-left: 8px;
  color: #666;
  font-size: 14px;
}

.item-comment {
  grid-column: 1 / -1;
}

.calculated-total {
  text-align: center;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 6px;
  margin-bottom: 32px;
}

.calculated-total h4 {
  margin: 0;
  color: #409eff;
  font-size: 18px;
}

.submit-section {
  text-align: center;
  padding-top: 20px;
  border-top: 1px solid #eee;
}

.submit-section .el-button {
  margin: 0 8px;
}
</style>