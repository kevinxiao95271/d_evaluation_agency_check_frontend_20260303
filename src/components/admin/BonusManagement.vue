<template>
  <div class="bonus-management">
    <div class="section-header">
      <h3>附加项管理</h3>
      <div class="header-actions">
        <el-select v-model="selectedTaskId" placeholder="选择考核任务" @change="loadBonusData">
          <el-option 
            v-for="task in tasks" 
            :key="task.id" 
            :label="task.name" 
            :value="task.id" 
          />
        </el-select>
      </div>
    </div>

    <!-- 说明信息 -->
    <el-alert
      title="附加项说明"
      type="info"
      :closable="false"
      show-icon
    >
      <template #default>
        <p>• 主任演讲：机构主任参与演讲展示，加8分</p>
        <p>• 秘书参与：机构秘书参与会务工作，加2分</p>
      </template>
    </el-alert>

    <!-- 机构附加项列表 -->
    <div class="bonus-table" v-loading="loading">
      <el-table :data="bonusData" stripe border>
        <el-table-column prop="institutionName" label="机构名称" min-width="200" />
        
        <el-table-column label="主任演讲" width="120" align="center">
          <template #default="{ row }">
            <el-switch
              v-model="row.directorPresentation"
              :active-value="1"
              :inactive-value="0"
              @change="updateBonus(row)"
            />
          </template>
        </el-table-column>
        
        <el-table-column label="秘书参与" width="120" align="center">
          <template #default="{ row }">
            <el-switch
              v-model="row.secretaryParticipation"
              :active-value="1"
              :inactive-value="0"
              @change="updateBonus(row)"
            />
          </template>
        </el-table-column>
        
        <el-table-column label="附加分" width="100" align="center">
          <template #default="{ row }">
            <el-tag type="success">
              +{{ (row.directorPresentation * 8) + (row.secretaryParticipation * 2) }} 分
            </el-tag>
          </template>
        </el-table-column>
        
        <el-table-column prop="filledBy" label="操作人" width="120" />
        
        <el-table-column prop="updateTime" label="更新时间" width="180" />
        
        <el-table-column label="操作" width="150" fixed="right">
          <template #default="{ row }">
            <el-button size="small" @click="editBonus(row)" :icon="Edit">
              编辑
            </el-button>
            <el-button size="small" @click="viewHistory(row)" :icon="View">
              历史
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <!-- 批量操作 -->
    <div class="batch-actions">
      <el-button @click="batchSetDirector" :icon="Check">批量设置主任演讲</el-button>
      <el-button @click="batchSetSecretary" :icon="Check">批量设置秘书参与</el-button>
      <el-button @click="batchClear" :icon="Close">批量清空</el-button>
    </div>

    <!-- 编辑对话框 -->
    <el-dialog title="编辑附加项" v-model="editVisible" width="500px">
      <el-form :model="editForm" label-width="120px">
        <el-form-item label="机构名称">
          <el-input :value="editForm.institutionName" disabled />
        </el-form-item>
        <el-form-item label="主任演讲">
          <el-radio-group v-model="editForm.directorPresentation">
            <el-radio :label="1">是 (+8分)</el-radio>
            <el-radio :label="0">否</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="秘书参与">
          <el-radio-group v-model="editForm.secretaryParticipation">
            <el-radio :label="1">是 (+2分)</el-radio>
            <el-radio :label="0">否</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="备注">
          <el-input 
            v-model="editForm.remark" 
            type="textarea" 
            :rows="3"
            placeholder="可选填写备注信息"
          />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="editVisible = false">取消</el-button>
        <el-button type="primary" @click="saveBonus" :loading="saving">
          {{ saving ? '保存中...' : '确定' }}
        </el-button>
      </template>
    </el-dialog>

    <!-- 历史记录对话框 -->
    <el-dialog title="操作历史" v-model="historyVisible" width="600px">
      <el-timeline>
        <el-timeline-item
          v-for="record in historyRecords"
          :key="record.id"
          :timestamp="record.updateTime"
        >
          <div class="history-item">
            <p><strong>操作人：</strong>{{ record.filledBy }}</p>
            <p><strong>主任演讲：</strong>{{ record.directorPresentation ? '是' : '否' }}</p>
            <p><strong>秘书参与：</strong>{{ record.secretaryParticipation ? '是' : '否' }}</p>
            <p v-if="record.remark"><strong>备注：</strong>{{ record.remark }}</p>
          </div>
        </el-timeline-item>
      </el-timeline>
    </el-dialog>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Edit, View, Check, Close } from '@element-plus/icons-vue'
import { taskApi, institutionApi } from '../../api'

export default {
  name: 'BonusManagement',
  components: { Edit, View, Check, Close },
  setup() {
    const loading = ref(false)
    const saving = ref(false)
    const editVisible = ref(false)
    const historyVisible = ref(false)
    const selectedTaskId = ref(null)
    
    const tasks = ref([])
    const bonusData = ref([])
    const historyRecords = ref([])
    
    const editForm = ref({
      taskId: null,
      institutionId: null,
      institutionName: '',
      directorPresentation: 0,
      secretaryParticipation: 0,
      remark: ''
    })
    
    const loadTasks = async () => {
      try {
        const data = await taskApi.getList()
        tasks.value = data || []
        
        if (tasks.value.length > 0) {
          selectedTaskId.value = tasks.value[0].id
          loadBonusData()
        }
      } catch (error) {
        console.error('加载任务列表失败:', error)
        ElMessage.error('加载任务列表失败')
      }
    }
    
    const loadBonusData = async () => {
      if (!selectedTaskId.value) return
      
      try {
        loading.value = true
        
        // 获取机构列表
        const institutions = await institutionApi.getList()
        
        // 模拟附加项数据
        bonusData.value = institutions.map(inst => ({
          taskId: selectedTaskId.value,
          institutionId: inst.id,
          institutionName: inst.name,
          directorPresentation: 0,
          secretaryParticipation: 0,
          filledBy: '',
          updateTime: '',
          remark: ''
        }))
        
      } catch (error) {
        console.error('加载附加项数据失败:', error)
        ElMessage.error('加载附加项数据失败')
      } finally {
        loading.value = false
      }
    }
    
    const updateBonus = async (row) => {
      try {
        // 调用更新API
        // await bonusApi.update(row)
        
        row.filledBy = '管理员'
        row.updateTime = new Date().toLocaleString()
        
        ElMessage.success('更新成功')
      } catch (error) {
        console.error('更新附加项失败:', error)
        ElMessage.error('更新附加项失败')
      }
    }
    
    const editBonus = (row) => {
      editForm.value = { ...row }
      editVisible.value = true
    }
    
    const saveBonus = async () => {
      try {
        saving.value = true
        
        // 调用保存API
        // await bonusApi.save(editForm.value)
        
        // 更新本地数据
        const index = bonusData.value.findIndex(item => 
          item.institutionId === editForm.value.institutionId
        )
        if (index !== -1) {
          bonusData.value[index] = {
            ...editForm.value,
            filledBy: '管理员',
            updateTime: new Date().toLocaleString()
          }
        }
        
        editVisible.value = false
        ElMessage.success('保存成功')
      } catch (error) {
        console.error('保存附加项失败:', error)
        ElMessage.error('保存附加项失败')
      } finally {
        saving.value = false
      }
    }
    
    const viewHistory = (row) => {
      // 模拟历史记录
      historyRecords.value = [
        {
          id: 1,
          filledBy: '管理员',
          directorPresentation: 1,
          secretaryParticipation: 0,
          updateTime: '2026-03-04 10:30:00',
          remark: '主任确认参与演讲'
        },
        {
          id: 2,
          filledBy: '系统管理员',
          directorPresentation: 0,
          secretaryParticipation: 0,
          updateTime: '2026-03-01 09:00:00',
          remark: '初始化数据'
        }
      ]
      
      historyVisible.value = true
    }
    
    const batchSetDirector = async () => {
      try {
        await ElMessageBox.confirm(
          '确定要为所有机构设置主任演讲吗？',
          '批量操作确认',
          { confirmButtonText: '确定', cancelButtonText: '取消', type: 'warning' }
        )
        
        bonusData.value.forEach(item => {
          item.directorPresentation = 1
          item.filledBy = '管理员'
          item.updateTime = new Date().toLocaleString()
        })
        
        ElMessage.success('批量设置成功')
      } catch (error) {
        if (error !== 'cancel') {
          ElMessage.error('批量设置失败')
        }
      }
    }
    
    const batchSetSecretary = async () => {
      try {
        await ElMessageBox.confirm(
          '确定要为所有机构设置秘书参与吗？',
          '批量操作确认',
          { confirmButtonText: '确定', cancelButtonText: '取消', type: 'warning' }
        )
        
        bonusData.value.forEach(item => {
          item.secretaryParticipation = 1
          item.filledBy = '管理员'
          item.updateTime = new Date().toLocaleString()
        })
        
        ElMessage.success('批量设置成功')
      } catch (error) {
        if (error !== 'cancel') {
          ElMessage.error('批量设置失败')
        }
      }
    }
    
    const batchClear = async () => {
      try {
        await ElMessageBox.confirm(
          '确定要清空所有机构的附加项吗？',
          '批量操作确认',
          { confirmButtonText: '确定', cancelButtonText: '取消', type: 'warning' }
        )
        
        bonusData.value.forEach(item => {
          item.directorPresentation = 0
          item.secretaryParticipation = 0
          item.filledBy = '管理员'
          item.updateTime = new Date().toLocaleString()
        })
        
        ElMessage.success('批量清空成功')
      } catch (error) {
        if (error !== 'cancel') {
          ElMessage.error('批量清空失败')
        }
      }
    }
    
    onMounted(() => {
      loadTasks()
    })
    
    return {
      loading, saving, editVisible, historyVisible, selectedTaskId,
      tasks, bonusData, historyRecords, editForm,
      loadBonusData, updateBonus, editBonus, saveBonus, viewHistory,
      batchSetDirector, batchSetSecretary, batchClear
    }
  }
}
</script>

<style scoped>
.bonus-management {
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

.bonus-table {
  margin: 20px 0;
}

.batch-actions {
  margin-top: 20px;
  padding: 16px;
  background: #f8f9fa;
  border-radius: 6px;
}

.batch-actions .el-button {
  margin-right: 12px;
}

.history-item p {
  margin: 4px 0;
  color: #666;
}
</style>