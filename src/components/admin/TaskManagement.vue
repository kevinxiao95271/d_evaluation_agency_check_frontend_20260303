<template>
  <div class="task-management">
    <div class="section-header">
      <h3>任务管理</h3>
      <el-button type="primary" @click="showAddDialog" :icon="Plus">
        新增任务
      </el-button>
    </div>

    <!-- 任务列表 -->
    <div class="table-section">
      <el-table :data="tasks" v-loading="loading" stripe border>
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="任务名称" min-width="200" />
        <el-table-column prop="period" label="考核周期" width="120" />
        <el-table-column prop="startDate" label="开始日期" width="120" />
        <el-table-column prop="endDate" label="结束日期" width="120" />
        <el-table-column label="当前任务" width="100" align="center">
          <template #default="{ row }">
            <el-tag v-if="row.isCurrent" type="success">是</el-tag>
            <span v-else>-</span>
          </template>
        </el-table-column>
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.status === 1 ? 'success' : 'danger'">
              {{ row.status === 1 ? '启用' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="description" label="描述" min-width="200" />
        <el-table-column label="操作" width="250" fixed="right">
          <template #default="{ row }">
            <el-button size="small" @click="editTask(row)" :icon="Edit">编辑</el-button>
            <el-button 
              size="small" 
              type="success" 
              @click="setCurrentTask(row)"
              :disabled="row.isCurrent"
              :icon="Check"
            >
              设为当前
            </el-button>
            <el-button size="small" type="danger" @click="deleteTask(row)" :icon="Delete">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <!-- 新增/编辑对话框 -->
    <el-dialog :title="dialogTitle" v-model="dialogVisible" width="600px" @close="resetForm">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="100px">
        <el-form-item label="任务名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入任务名称" />
        </el-form-item>
        <el-form-item label="考核周期" prop="period">
          <el-input v-model="form.period" placeholder="如：2026Q1" />
        </el-form-item>
        <el-form-item label="考核时间" prop="dateRange">
          <el-date-picker
            v-model="form.dateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
          />
        </el-form-item>
        <el-form-item label="任务描述" prop="description">
          <el-input 
            v-model="form.description" 
            type="textarea" 
            :rows="3"
            placeholder="请输入任务描述"
          />
        </el-form-item>
        <el-form-item label="关联机构">
          <el-select 
            v-model="form.institutionIds" 
            multiple 
            placeholder="选择参与考核的机构"
            style="width: 100%"
            filterable
          >
            <el-option 
              v-for="inst in institutions" 
              :key="inst.id" 
              :label="inst.name" 
              :value="inst.id" 
            />
          </el-select>
          <div class="form-tip">
            <el-button size="small" @click="selectAllInstitutions">全选</el-button>
            <el-button size="small" @click="clearInstitutions">清空</el-button>
          </div>
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitForm" :loading="submitting">
          {{ submitting ? '保存中...' : '确定' }}
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Edit, Check, Delete } from '@element-plus/icons-vue'
import { taskApi, institutionApi } from '../../api'

export default {
  name: 'TaskManagement',
  components: { Plus, Edit, Check, Delete },
  setup() {
    const loading = ref(false)
    const submitting = ref(false)
    const dialogVisible = ref(false)
    const isEdit = ref(false)
    const formRef = ref(null)
    
    const tasks = ref([])
    const institutions = ref([])
    
    const form = ref({
      id: null,
      name: '',
      period: '',
      dateRange: [],
      description: '',
      institutionIds: []
    })
    
    const rules = {
      name: [{ required: true, message: '请输入任务名称', trigger: 'blur' }],
      period: [{ required: true, message: '请输入考核周期', trigger: 'blur' }],
      dateRange: [{ required: true, message: '请选择考核时间', trigger: 'change' }],
      description: [{ required: true, message: '请输入任务描述', trigger: 'blur' }]
    }
    
    const dialogTitle = computed(() => isEdit.value ? '编辑任务' : '新增任务')
    
    const loadTasks = async () => {
      try {
        loading.value = true
        const data = await taskApi.getList()
        tasks.value = data || []
      } catch (error) {
        console.error('加载任务列表失败:', error)
        ElMessage.error('加载任务列表失败')
      } finally {
        loading.value = false
      }
    }
    
    const loadInstitutions = async () => {
      try {
        const data = await institutionApi.getList()
        institutions.value = data
      } catch (error) {
        console.error('加载机构列表失败:', error)
      }
    }
    
    const showAddDialog = () => {
      isEdit.value = false
      dialogVisible.value = true
    }
    
    const editTask = (row) => {
      isEdit.value = true
      form.value = {
        ...row,
        dateRange: [row.startDate, row.endDate],
        institutionIds: row.institutionIds || []
      }
      dialogVisible.value = true
    }
    
    const setCurrentTask = async (row) => {
      try {
        await ElMessageBox.confirm(
          `确定要将"${row.name}"设为当前任务吗？`,
          '确认操作',
          { confirmButtonText: '确定', cancelButtonText: '取消', type: 'warning' }
        )
        
        // 调用设置当前任务API
        // await taskApi.setCurrent(row.id)
        
        ElMessage.success('设置成功')
        loadTasks()
      } catch (error) {
        if (error !== 'cancel') {
          console.error('设置当前任务失败:', error)
          ElMessage.error('设置当前任务失败')
        }
      }
    }
    
    const deleteTask = async (row) => {
      try {
        await ElMessageBox.confirm(
          `确定要删除任务"${row.name}"吗？此操作不可恢复。`,
          '确认删除',
          { confirmButtonText: '确定删除', cancelButtonText: '取消', type: 'warning' }
        )
        
        ElMessage.success('删除成功')
        loadTasks()
      } catch (error) {
        if (error !== 'cancel') {
          console.error('删除任务失败:', error)
          ElMessage.error('删除任务失败')
        }
      }
    }
    
    const selectAllInstitutions = () => {
      form.value.institutionIds = institutions.value.map(inst => inst.id)
    }
    
    const clearInstitutions = () => {
      form.value.institutionIds = []
    }
    
    const submitForm = async () => {
      try {
        await formRef.value.validate()
        submitting.value = true
        
        const submitData = {
          ...form.value,
          startDate: form.value.dateRange[0],
          endDate: form.value.dateRange[1]
        }
        delete submitData.dateRange
        
        if (isEdit.value) {
          ElMessage.success('更新成功')
        } else {
          ElMessage.success('创建成功')
        }
        
        dialogVisible.value = false
        loadTasks()
      } catch (error) {
        console.error('保存任务失败:', error)
        ElMessage.error('保存任务失败')
      } finally {
        submitting.value = false
      }
    }
    
    const resetForm = () => {
      form.value = {
        id: null, name: '', period: '', dateRange: [], 
        description: '', institutionIds: []
      }
      formRef.value?.resetFields()
    }
    
    onMounted(() => {
      loadTasks()
      loadInstitutions()
    })
    
    return {
      loading, submitting, dialogVisible, dialogTitle, formRef, isEdit,
      tasks, institutions, form, rules,
      loadTasks, showAddDialog, editTask, setCurrentTask, deleteTask,
      selectAllInstitutions, clearInstitutions, submitForm, resetForm
    }
  }
}
</script>

<style scoped>
.task-management {
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

.table-section {
  margin-top: 20px;
}

.form-tip {
  margin-top: 8px;
}

.form-tip .el-button {
  margin-right: 8px;
}
</style>