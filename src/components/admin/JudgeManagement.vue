<template>
  <div class="judge-management">
    <div class="section-header">
      <h3>评委管理</h3>
      <el-button type="primary" @click="showAddDialog" :icon="Plus">
        新增评委
      </el-button>
    </div>

    <!-- 筛选条件 -->
    <div class="filter-section">
      <el-form :inline="true" :model="filterForm" class="filter-form">
        <el-form-item label="评委类型">
          <el-select v-model="filterForm.type" placeholder="全部类型" clearable>
            <el-option label="专家评委" value="EXPERT" />
            <el-option label="大众评委" value="PUBLIC" />
          </el-select>
        </el-form-item>
        <el-form-item label="所属机构">
          <el-select v-model="filterForm.institutionId" placeholder="全部机构" clearable filterable>
            <el-option 
              v-for="inst in institutions" 
              :key="inst.id" 
              :label="inst.name" 
              :value="inst.id" 
            />
          </el-select>
        </el-form-item>
        <el-form-item label="评委姓名">
          <el-input v-model="filterForm.name" placeholder="请输入评委姓名" clearable />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="loadJudges" :icon="Search">查询</el-button>
          <el-button @click="resetFilter">重置</el-button>
        </el-form-item>
      </el-form>
    </div>

    <!-- 评委列表 -->
    <div class="table-section">
      <el-table :data="filteredJudges" v-loading="loading" stripe border>
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="姓名" width="120" />
        <el-table-column prop="username" label="用户名" width="120" />
        <el-table-column prop="type" label="类型" width="100">
          <template #default="{ row }">
            <el-tag :type="row.type === 'EXPERT' ? 'primary' : 'success'">
              {{ row.type === 'EXPERT' ? '专家评委' : '大众评委' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="title" label="职称" width="120" />
        <el-table-column prop="institutionName" label="所属机构" min-width="200" />
        <el-table-column prop="phone" label="联系电话" width="150" />
        <el-table-column prop="email" label="邮箱" width="180" />
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.status === 1 ? 'success' : 'danger'">
              {{ row.status === 1 ? '启用' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button size="small" @click="editJudge(row)" :icon="Edit">编辑</el-button>
            <el-button size="small" type="danger" @click="deleteJudge(row)" :icon="Delete">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <!-- 新增/编辑对话框 -->
    <el-dialog :title="dialogTitle" v-model="dialogVisible" width="600px" @close="resetForm">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="100px">
        <el-form-item label="姓名" prop="name">
          <el-input v-model="form.name" placeholder="请输入评委姓名" />
        </el-form-item>
        <el-form-item label="用户名" prop="username">
          <el-input v-model="form.username" placeholder="请输入登录用户名" />
        </el-form-item>
        <el-form-item label="密码" prop="password" v-if="!isEdit">
          <el-input v-model="form.password" type="password" placeholder="请输入登录密码" />
        </el-form-item>
        <el-form-item label="评委类型" prop="type">
          <el-select v-model="form.type" placeholder="请选择评委类型">
            <el-option label="专家评委" value="EXPERT" />
            <el-option label="大众评委" value="PUBLIC" />
          </el-select>
        </el-form-item>
        <el-form-item label="职称" prop="title">
          <el-input v-model="form.title" placeholder="请输入职称" />
        </el-form-item>
        <el-form-item label="所属机构" prop="institutionId">
          <el-select v-model="form.institutionId" placeholder="请选择所属机构" filterable>
            <el-option 
              v-for="inst in institutions" 
              :key="inst.id" 
              :label="inst.name" 
              :value="inst.id" 
            />
          </el-select>
        </el-form-item>
        <el-form-item label="联系电话" prop="phone">
          <el-input v-model="form.phone" placeholder="请输入联系电话" />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="form.email" placeholder="请输入邮箱地址" />
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
import { Plus, Search, Edit, Delete } from '@element-plus/icons-vue'
import { judgeApi, institutionApi } from '../../api'

export default {
  name: 'JudgeManagement',
  components: { Plus, Search, Edit, Delete },
  setup() {
    const loading = ref(false)
    const submitting = ref(false)
    const dialogVisible = ref(false)
    const isEdit = ref(false)
    const formRef = ref(null)
    
    const judges = ref([])
    const institutions = ref([])
    const filterForm = ref({
      type: '',
      institutionId: '',
      name: ''
    })
    
    const form = ref({
      id: null,
      name: '',
      username: '',
      password: '',
      type: '',
      title: '',
      institutionId: '',
      phone: '',
      email: ''
    })
    
    const rules = {
      name: [{ required: true, message: '请输入评委姓名', trigger: 'blur' }],
      username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
      password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
      type: [{ required: true, message: '请选择评委类型', trigger: 'change' }],
      institutionId: [{ required: true, message: '请选择所属机构', trigger: 'change' }]
    }
    
    const dialogTitle = computed(() => isEdit.value ? '编辑评委' : '新增评委')
    
    const filteredJudges = computed(() => {
      let result = judges.value
      
      if (filterForm.value.type) {
        result = result.filter(item => item.type === filterForm.value.type)
      }
      
      if (filterForm.value.institutionId) {
        result = result.filter(item => item.institutionId === filterForm.value.institutionId)
      }
      
      if (filterForm.value.name) {
        result = result.filter(item => item.name.includes(filterForm.value.name))
      }
      
      return result
    })
    
    const loadJudges = async () => {
      try {
        loading.value = true
        const data = await judgeApi.getList()
        judges.value = data
      } catch (error) {
        console.error('加载评委列表失败:', error)
        ElMessage.error('加载评委列表失败')
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
    
    const resetFilter = () => {
      filterForm.value = { type: '', institutionId: '', name: '' }
    }
    
    const showAddDialog = () => {
      isEdit.value = false
      dialogVisible.value = true
    }
    
    const editJudge = (row) => {
      isEdit.value = true
      form.value = { ...row }
      dialogVisible.value = true
    }
    
    const deleteJudge = async (row) => {
      try {
        await ElMessageBox.confirm(
          `确定要删除评委"${row.name}"吗？此操作不可恢复。`,
          '确认删除',
          { confirmButtonText: '确定删除', cancelButtonText: '取消', type: 'warning' }
        )
        
        ElMessage.success('删除成功')
        loadJudges()
      } catch (error) {
        if (error !== 'cancel') {
          console.error('删除评委失败:', error)
          ElMessage.error('删除评委失败')
        }
      }
    }
    
    const submitForm = async () => {
      try {
        await formRef.value.validate()
        submitting.value = true
        
        if (isEdit.value) {
          ElMessage.success('更新成功')
        } else {
          ElMessage.success('创建成功')
        }
        
        dialogVisible.value = false
        loadJudges()
      } catch (error) {
        console.error('保存评委失败:', error)
        ElMessage.error('保存评委失败')
      } finally {
        submitting.value = false
      }
    }
    
    const resetForm = () => {
      form.value = {
        id: null, name: '', username: '', password: '', 
        type: '', title: '', institutionId: '', phone: '', email: ''
      }
      formRef.value?.resetFields()
    }
    
    onMounted(() => {
      loadJudges()
      loadInstitutions()
    })
    
    return {
      loading, submitting, dialogVisible, dialogTitle, formRef,
      judges, institutions, filteredJudges, filterForm, form, rules, isEdit,
      loadJudges, resetFilter, showAddDialog, editJudge, deleteJudge, submitForm, resetForm
    }
  }
}
</script>

<style scoped>
.judge-management {
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

.filter-section {
  margin-bottom: 20px;
  padding: 16px;
  background: #f8f9fa;
  border-radius: 6px;
}

.filter-form .el-form-item {
  margin-bottom: 0;
}

.table-section {
  margin-top: 20px;
}
</style>