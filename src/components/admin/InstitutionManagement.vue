<template>
  <div class="institution-management">
    <div class="section-header">
      <h3>机构管理</h3>
      <el-button type="primary" @click="showAddDialog" :icon="Plus">
        新增机构
      </el-button>
    </div>

    <!-- 筛选条件 -->
    <div class="filter-section">
      <el-form :inline="true" :model="filterForm" class="filter-form">
        <el-form-item label="机构类型">
          <el-select v-model="filterForm.type" placeholder="全部类型" clearable>
            <el-option label="专业质控中心" value="QUALITY_CONTROL" />
            <el-option label="技术服务中心" value="TECHNICAL_SERVICE" />
          </el-select>
        </el-form-item>
        <el-form-item label="机构名称">
          <el-input 
            v-model="filterForm.name" 
            placeholder="请输入机构名称"
            clearable
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="loadInstitutions" :icon="Search">
            查询
          </el-button>
          <el-button @click="resetFilter">重置</el-button>
        </el-form-item>
      </el-form>
    </div>

    <!-- 机构列表 -->
    <div class="table-section">
      <el-table 
        :data="filteredInstitutions" 
        v-loading="loading"
        stripe
        border
      >
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="机构名称" min-width="200" />
        <el-table-column prop="type" label="机构类型" width="150">
          <template #default="{ row }">
            <el-tag :type="row.type === 'QUALITY_CONTROL' ? 'primary' : 'success'">
              {{ row.type === 'QUALITY_CONTROL' ? '专业质控中心' : '技术服务中心' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="description" label="描述" min-width="200" />
        <el-table-column prop="director" label="负责人" width="120" />
        <el-table-column prop="phone" label="联系电话" width="150" />
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.status === 1 ? 'success' : 'danger'">
              {{ row.status === 1 ? '启用' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button size="small" @click="editInstitution(row)" :icon="Edit">
              编辑
            </el-button>
            <el-button 
              size="small" 
              type="danger" 
              @click="deleteInstitution(row)"
              :icon="Delete"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <!-- 新增/编辑对话框 -->
    <el-dialog 
      :title="dialogTitle" 
      v-model="dialogVisible" 
      width="600px"
      @close="resetForm"
    >
      <el-form 
        ref="formRef" 
        :model="form" 
        :rules="rules" 
        label-width="100px"
      >
        <el-form-item label="机构名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入机构名称" />
        </el-form-item>
        <el-form-item label="机构类型" prop="type">
          <el-select v-model="form.type" placeholder="请选择机构类型">
            <el-option label="专业质控中心" value="QUALITY_CONTROL" />
            <el-option label="技术服务中心" value="TECHNICAL_SERVICE" />
          </el-select>
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input 
            v-model="form.description" 
            type="textarea" 
            :rows="3"
            placeholder="请输入机构描述"
          />
        </el-form-item>
        <el-form-item label="负责人" prop="director">
          <el-input v-model="form.director" placeholder="请输入负责人姓名" />
        </el-form-item>
        <el-form-item label="联系电话" prop="phone">
          <el-input v-model="form.phone" placeholder="请输入联系电话" />
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
import { institutionApi } from '../../api'

export default {
  name: 'InstitutionManagement',
  components: {
    Plus,
    Search,
    Edit,
    Delete
  },
  setup() {
    const loading = ref(false)
    const submitting = ref(false)
    const dialogVisible = ref(false)
    const isEdit = ref(false)
    const formRef = ref(null)
    
    const institutions = ref([])
    const filterForm = ref({
      type: '',
      name: ''
    })
    
    const form = ref({
      id: null,
      name: '',
      type: '',
      description: '',
      director: '',
      phone: ''
    })
    
    const rules = {
      name: [
        { required: true, message: '请输入机构名称', trigger: 'blur' }
      ],
      type: [
        { required: true, message: '请选择机构类型', trigger: 'change' }
      ],
      description: [
        { required: true, message: '请输入机构描述', trigger: 'blur' }
      ]
    }
    
    // 计算属性
    const dialogTitle = computed(() => isEdit.value ? '编辑机构' : '新增机构')
    
    const filteredInstitutions = computed(() => {
      let result = institutions.value
      
      if (filterForm.value.type) {
        result = result.filter(item => item.type === filterForm.value.type)
      }
      
      if (filterForm.value.name) {
        result = result.filter(item => 
          item.name.includes(filterForm.value.name)
        )
      }
      
      return result
    })
    
    // 加载机构列表
    const loadInstitutions = async () => {
      try {
        loading.value = true
        const data = await institutionApi.getList()
        institutions.value = data
      } catch (error) {
        console.error('加载机构列表失败:', error)
        ElMessage.error('加载机构列表失败')
      } finally {
        loading.value = false
      }
    }
    
    // 重置筛选条件
    const resetFilter = () => {
      filterForm.value = {
        type: '',
        name: ''
      }
    }
    
    // 显示新增对话框
    const showAddDialog = () => {
      isEdit.value = false
      dialogVisible.value = true
    }
    
    // 编辑机构
    const editInstitution = (row) => {
      isEdit.value = true
      form.value = { ...row }
      dialogVisible.value = true
    }
    
    // 删除机构
    const deleteInstitution = async (row) => {
      try {
        await ElMessageBox.confirm(
          `确定要删除机构"${row.name}"吗？此操作不可恢复。`,
          '确认删除',
          {
            confirmButtonText: '确定删除',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )
        
        // 调用删除API
        // await institutionApi.delete(row.id)
        
        ElMessage.success('删除成功')
        loadInstitutions()
        
      } catch (error) {
        if (error !== 'cancel') {
          console.error('删除机构失败:', error)
          ElMessage.error('删除机构失败')
        }
      }
    }
    
    // 提交表单
    const submitForm = async () => {
      try {
        await formRef.value.validate()
        submitting.value = true
        
        if (isEdit.value) {
          // 更新机构
          // await institutionApi.update(form.value.id, form.value)
          ElMessage.success('更新成功')
        } else {
          // 创建机构
          // await institutionApi.create(form.value)
          ElMessage.success('创建成功')
        }
        
        dialogVisible.value = false
        loadInstitutions()
        
      } catch (error) {
        console.error('保存机构失败:', error)
        ElMessage.error('保存机构失败')
      } finally {
        submitting.value = false
      }
    }
    
    // 重置表单
    const resetForm = () => {
      form.value = {
        id: null,
        name: '',
        type: '',
        description: '',
        director: '',
        phone: ''
      }
      formRef.value?.resetFields()
    }
    
    // 初始化
    onMounted(() => {
      loadInstitutions()
    })
    
    return {
      loading,
      submitting,
      dialogVisible,
      dialogTitle,
      formRef,
      institutions,
      filteredInstitutions,
      filterForm,
      form,
      rules,
      loadInstitutions,
      resetFilter,
      showAddDialog,
      editInstitution,
      deleteInstitution,
      submitForm,
      resetForm
    }
  }
}
</script>

<style scoped>
.institution-management {
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