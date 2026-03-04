<template>
  <div class="system-config">
    <div class="section-header">
      <h3>系统配置</h3>
    </div>

    <!-- 配置表单 -->
    <div class="config-form">
      <el-form :model="configForm" label-width="150px" size="large">
        
        <!-- 评分配置 -->
        <el-card class="config-card">
          <template #header>
            <h4>评分配置</h4>
          </template>
          
          <el-form-item label="系统总分">
            <div class="config-item">
              <el-input-number 
                v-model="configForm.systemTotalScore" 
                :min="1" 
                :max="1000"
                :precision="1"
                style="width: 200px;"
              />
              <span class="config-desc">分 - 评委评分换算到系统的总分值</span>
            </div>
          </el-form-item>
          
          <el-form-item label="专家权重">
            <div class="config-item">
              <el-input-number 
                v-model="configForm.expertWeight" 
                :min="0" 
                :max="1"
                :step="0.01"
                :precision="2"
                style="width: 200px;"
              />
              <span class="config-desc">- 专家评委评分在最终得分中的权重</span>
            </div>
          </el-form-item>
          
          <el-form-item label="大众权重">
            <div class="config-item">
              <el-input-number 
                v-model="configForm.publicWeight" 
                :min="0" 
                :max="1"
                :step="0.01"
                :precision="2"
                style="width: 200px;"
              />
              <span class="config-desc">- 大众评委评分在最终得分中的权重</span>
            </div>
          </el-form-item>
          
          <el-form-item label="去极值设置">
            <div class="config-item">
              <el-switch 
                v-model="configForm.removeExtremes"
                active-text="启用"
                inactive-text="禁用"
              />
              <span class="config-desc">- 是否去掉最高分和最低分后计算平均分</span>
            </div>
          </el-form-item>
        </el-card>

        <!-- 附加分配置 -->
        <el-card class="config-card">
          <template #header>
            <h4>附加分配置</h4>
          </template>
          
          <el-form-item label="主任演讲加分">
            <div class="config-item">
              <el-input-number 
                v-model="configForm.directorBonusScore" 
                :min="0" 
                :max="50"
                :precision="1"
                style="width: 200px;"
              />
              <span class="config-desc">分 - 机构主任参与演讲的加分</span>
            </div>
          </el-form-item>
          
          <el-form-item label="秘书参与加分">
            <div class="config-item">
              <el-input-number 
                v-model="configForm.secretaryBonusScore" 
                :min="0" 
                :max="50"
                :precision="1"
                style="width: 200px;"
              />
              <span class="config-desc">分 - 机构秘书参与会务的加分</span>
            </div>
          </el-form-item>
        </el-card>

        <!-- 系统设置 -->
        <el-card class="config-card">
          <template #header>
            <h4>系统设置</h4>
          </template>
          
          <el-form-item label="系统名称">
            <div class="config-item">
              <el-input 
                v-model="configForm.systemName" 
                style="width: 300px;"
                placeholder="请输入系统名称"
              />
            </div>
          </el-form-item>
          
          <el-form-item label="评分截止时间">
            <div class="config-item">
              <el-switch 
                v-model="configForm.enableDeadline"
                active-text="启用"
                inactive-text="禁用"
              />
              <span class="config-desc">- 是否启用评分截止时间限制</span>
            </div>
          </el-form-item>
          
          <el-form-item label="允许修改评分" v-if="configForm.enableDeadline">
            <div class="config-item">
              <el-switch 
                v-model="configForm.allowModifyScore"
                active-text="允许"
                inactive-text="禁止"
              />
              <span class="config-desc">- 截止时间前是否允许修改已提交的评分</span>
            </div>
          </el-form-item>
          
          <el-form-item label="自动计算结果">
            <div class="config-item">
              <el-switch 
                v-model="configForm.autoCalculate"
                active-text="启用"
                inactive-text="禁用"
              />
              <span class="config-desc">- 评分提交后是否自动计算和更新结果</span>
            </div>
          </el-form-item>
        </el-card>

        <!-- 通知设置 -->
        <el-card class="config-card">
          <template #header>
            <h4>通知设置</h4>
          </template>
          
          <el-form-item label="邮件通知">
            <div class="config-item">
              <el-switch 
                v-model="configForm.emailNotification"
                active-text="启用"
                inactive-text="禁用"
              />
              <span class="config-desc">- 是否启用邮件通知功能</span>
            </div>
          </el-form-item>
          
          <el-form-item label="SMTP服务器" v-if="configForm.emailNotification">
            <div class="config-item">
              <el-input 
                v-model="configForm.smtpServer" 
                style="width: 300px;"
                placeholder="请输入SMTP服务器地址"
              />
            </div>
          </el-form-item>
          
          <el-form-item label="发件人邮箱" v-if="configForm.emailNotification">
            <div class="config-item">
              <el-input 
                v-model="configForm.senderEmail" 
                style="width: 300px;"
                placeholder="请输入发件人邮箱"
              />
            </div>
          </el-form-item>
        </el-card>

        <!-- 保存按钮 -->
        <div class="save-actions">
          <el-button type="primary" @click="saveConfig" :loading="saving" size="large">
            {{ saving ? '保存中...' : '保存配置' }}
          </el-button>
          <el-button @click="resetConfig" size="large">重置</el-button>
          <el-button @click="exportConfig" :icon="Download" size="large">导出配置</el-button>
          <el-button @click="importConfig" :icon="Upload" size="large">导入配置</el-button>
        </div>
      </el-form>
    </div>

    <!-- 导入配置对话框 -->
    <el-dialog title="导入配置" v-model="importVisible" width="500px">
      <el-upload
        class="upload-demo"
        drag
        :auto-upload="false"
        :on-change="handleFileChange"
        accept=".json"
      >
        <el-icon class="el-icon--upload"><upload-filled /></el-icon>
        <div class="el-upload__text">
          将配置文件拖到此处，或<em>点击上传</em>
        </div>
        <template #tip>
          <div class="el-upload__tip">
            只能上传 JSON 格式的配置文件
          </div>
        </template>
      </el-upload>
      
      <template #footer>
        <el-button @click="importVisible = false">取消</el-button>
        <el-button type="primary" @click="confirmImport" :loading="importing">
          {{ importing ? '导入中...' : '确定导入' }}
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Download, Upload } from '@element-plus/icons-vue'

export default {
  name: 'SystemConfig',
  components: { Download, Upload },
  setup() {
    const saving = ref(false)
    const importing = ref(false)
    const importVisible = ref(false)
    const importFile = ref(null)
    
    const configForm = ref({
      // 评分配置
      systemTotalScore: 45,
      expertWeight: 0.7,
      publicWeight: 0.2,
      removeExtremes: true,
      
      // 附加分配置
      directorBonusScore: 8,
      secretaryBonusScore: 2,
      
      // 系统设置
      systemName: '机构考核评估系统',
      enableDeadline: false,
      allowModifyScore: true,
      autoCalculate: true,
      
      // 通知设置
      emailNotification: false,
      smtpServer: '',
      senderEmail: ''
    })
    
    const originalConfig = ref({})
    
    const loadConfig = async () => {
      try {
        // 调用获取配置API
        // const data = await systemConfigApi.getAll()
        // configForm.value = { ...data }
        
        // 保存原始配置用于重置
        originalConfig.value = JSON.parse(JSON.stringify(configForm.value))
        
      } catch (error) {
        console.error('加载系统配置失败:', error)
        ElMessage.error('加载系统配置失败')
      }
    }
    
    const saveConfig = async () => {
      try {
        // 验证权重总和
        const totalWeight = configForm.value.expertWeight + configForm.value.publicWeight
        if (Math.abs(totalWeight - 1) > 0.01) {
          ElMessage.warning('专家权重和大众权重之和应该等于1')
          return
        }
        
        saving.value = true
        
        // 调用保存配置API
        // await systemConfigApi.saveAll(configForm.value)
        
        ElMessage.success('配置保存成功')
        
        // 更新原始配置
        originalConfig.value = JSON.parse(JSON.stringify(configForm.value))
        
      } catch (error) {
        console.error('保存系统配置失败:', error)
        ElMessage.error('保存系统配置失败')
      } finally {
        saving.value = false
      }
    }
    
    const resetConfig = () => {
      configForm.value = JSON.parse(JSON.stringify(originalConfig.value))
      ElMessage.info('配置已重置')
    }
    
    const exportConfig = () => {
      try {
        const configData = JSON.stringify(configForm.value, null, 2)
        const blob = new Blob([configData], { type: 'application/json' })
        const url = URL.createObjectURL(blob)
        
        const link = document.createElement('a')
        link.href = url
        link.download = `system-config-${new Date().toISOString().split('T')[0]}.json`
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
        
        URL.revokeObjectURL(url)
        ElMessage.success('配置导出成功')
        
      } catch (error) {
        console.error('导出配置失败:', error)
        ElMessage.error('导出配置失败')
      }
    }
    
    const importConfig = () => {
      importVisible.value = true
    }
    
    const handleFileChange = (file) => {
      importFile.value = file.raw
    }
    
    const confirmImport = async () => {
      if (!importFile.value) {
        ElMessage.warning('请选择配置文件')
        return
      }
      
      try {
        importing.value = true
        
        const text = await importFile.value.text()
        const importedConfig = JSON.parse(text)
        
        // 验证配置格式
        if (!importedConfig.systemTotalScore) {
          throw new Error('配置文件格式不正确')
        }
        
        configForm.value = { ...configForm.value, ...importedConfig }
        
        importVisible.value = false
        ElMessage.success('配置导入成功')
        
      } catch (error) {
        console.error('导入配置失败:', error)
        ElMessage.error('导入配置失败：' + error.message)
      } finally {
        importing.value = false
      }
    }
    
    onMounted(() => {
      loadConfig()
    })
    
    return {
      saving, importing, importVisible, configForm,
      saveConfig, resetConfig, exportConfig, importConfig,
      handleFileChange, confirmImport
    }
  }
}
</script>

<style scoped>
.system-config {
  height: 100%;
}

.section-header {
  margin-bottom: 20px;
}

.section-header h3 {
  margin: 0;
  color: #333;
}

.config-form {
  max-width: 800px;
}

.config-card {
  margin-bottom: 24px;
}

.config-card h4 {
  margin: 0;
  color: #333;
  font-size: 16px;
}

.config-item {
  display: flex;
  align-items: center;
}

.config-desc {
  margin-left: 12px;
  color: #666;
  font-size: 14px;
}

.save-actions {
  text-align: center;
  padding: 24px 0;
  border-top: 1px solid #eee;
  margin-top: 24px;
}

.save-actions .el-button {
  margin: 0 8px;
}

.upload-demo {
  margin: 20px 0;
}
</style>