<template>
  <div class="api-test">
    <h2>API 测试页面</h2>
    
    <div class="test-section">
      <h3>1. 评分提交测试</h3>
      <el-button @click="testScoreSubmit" type="primary">测试评分提交</el-button>
      <pre v-if="scoreResult">{{ scoreResult }}</pre>
    </div>
    
    <div class="test-section">
      <h3>2. 系统配置测试</h3>
      <el-button @click="testSystemConfig" type="primary">测试系统配置</el-button>
      <pre v-if="configResult">{{ configResult }}</pre>
    </div>
    
    <div class="test-section">
      <h3>3. 附加项测试</h3>
      <el-button @click="testBonus" type="primary">测试附加项</el-button>
      <pre v-if="bonusResult">{{ bonusResult }}</pre>
    </div>
    
    <div class="test-section">
      <h3>4. 结果统计测试</h3>
      <el-button @click="testResults" type="primary">测试结果统计</el-button>
      <pre v-if="resultsData">{{ resultsData }}</pre>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import axios from 'axios'

export default {
  name: 'ApiTest',
  setup() {
    const scoreResult = ref('')
    const configResult = ref('')
    const bonusResult = ref('')
    const resultsData = ref('')
    
    const testScoreSubmit = async () => {
      try {
        // 测试直接打总分
        const response1 = await axios.post('/api/score/submit', {
          taskId: 1,
          institutionId: 2,
          judgeId: 1,
          scoreMode: "TOTAL",
          totalScore: 42.5
        })
        
        // 测试逐条打分
        const response2 = await axios.post('/api/score/submit', {
          taskId: 1,
          institutionId: 3,
          judgeId: 1,
          scoreMode: "ITEM",
          itemScores: [
            {itemId: 1, score: 8.5, comment: "组织建设良好"},
            {itemId: 2, score: 9.0, comment: "制度完善"}
          ]
        })
        
        scoreResult.value = JSON.stringify({
          totalMode: response1.data,
          itemMode: response2.data
        }, null, 2)
        
      } catch (error) {
        scoreResult.value = `错误: ${error.message}\n${JSON.stringify(error.response?.data, null, 2)}`
      }
    }
    
    const testSystemConfig = async () => {
      try {
        const response1 = await axios.get('/api/system-config/total-score')
        const response2 = await axios.get('/api/system-config/list')
        
        configResult.value = JSON.stringify({
          totalScore: response1.data,
          allConfigs: response2.data
        }, null, 2)
        
      } catch (error) {
        configResult.value = `错误: ${error.message}\n${JSON.stringify(error.response?.data, null, 2)}`
      }
    }
    
    const testBonus = async () => {
      try {
        // 获取附加项
        const response1 = await axios.get('/api/bonus/1/2')
        
        // 设置附加项
        const response2 = await axios.post('/api/bonus', {
          taskId: 1,
          institutionId: 2,
          directorPresentation: 1,
          secretaryParticipation: 1,
          filledBy: "测试管理员"
        })
        
        bonusResult.value = JSON.stringify({
          getBonus: response1.data,
          setBonus: response2.data
        }, null, 2)
        
      } catch (error) {
        bonusResult.value = `错误: ${error.message}\n${JSON.stringify(error.response?.data, null, 2)}`
      }
    }
    
    const testResults = async () => {
      try {
        // 单个机构得分
        const response1 = await axios.get('/api/score/result?taskId=1&institutionId=2')
        
        // 所有机构得分
        const response2 = await axios.get('/api/score/results/1')
        
        resultsData.value = JSON.stringify({
          singleResult: response1.data,
          allResults: response2.data
        }, null, 2)
        
      } catch (error) {
        resultsData.value = `错误: ${error.message}\n${JSON.stringify(error.response?.data, null, 2)}`
      }
    }
    
    return {
      scoreResult,
      configResult,
      bonusResult,
      resultsData,
      testScoreSubmit,
      testSystemConfig,
      testBonus,
      testResults
    }
  }
}
</script>

<style scoped>
.api-test {
  padding: 20px;
  max-width: 1000px;
  margin: 0 auto;
}

.test-section {
  margin-bottom: 30px;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
}

.test-section h3 {
  margin-top: 0;
  color: #333;
}

pre {
  background: #f5f5f5;
  padding: 15px;
  border-radius: 4px;
  overflow-x: auto;
  font-size: 12px;
  line-height: 1.4;
  margin-top: 15px;
}
</style>