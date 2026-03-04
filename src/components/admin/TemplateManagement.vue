<template>
  <div class="template-management">
    <div class="section-header">
      <h3>评分表配置</h3>
      <el-button type="primary" @click="showAddDialog" :icon="Plus">
        新增模板
      </el-button>
    </div>

    <!-- 模板列表 -->
    <div class="template-list">
      <el-card 
        v-for="template in templates" 
        :key="template.id"
        class="template-card"
        :class="{ 'is-default': template.isDefault }"
      >
        <template #header>
          <div class="card-header">
            <span class="template-name">{{ template.name }}</span>
            <div class="card-actions">
              <el-tag v-if="template.isDefault" type="success">默认模板</el-tag>
              <el-button size="small" @click="editTemplate(template)" :icon="Edit">编辑</el-button>
              <el-button 
                size="small" 
                type="success" 
                @click="setDefault(template)"
                :disabled="template.isDefault"
                :icon="Check"
              >
                设为默认
              </el-button>
              <el-button size="small" type="danger" @click="deleteTemplate(template)" :icon="Delete">删除</el-button>
            </div>
          </div>
        </template>
        
        <div class="template-info">
          <p><strong>模板总分：</strong>{{ template.templateMaxScore }} 分</p>
          <p><strong>系统总分：</strong>{{ template.systemTotalScore }} 分</p>
          <p><strong>分类数量：</strong>{{ template.categories?.length || 0 }} 个</p>
          <p><strong>条目数量：</strong>{{ getTotalItems(template) }} 个</p>
        </div>
        
        <div class="categories-preview" v-if="template.categories">
          <h5>分类预览：</h5>
          <el-tag 
            v-for="category in template.categories" 
            :key="category.id"
            class="category-tag"
          >
            {{ category.name }} ({{ category.items?.length || 0 }}项)
          </el-tag>
        </div>
      </el-card>
    </div>

    <!-- 新增/编辑对话框 -->
    <el-dialog :title="dialogTitle" v-model="dialogVisible" width="800px" @close="resetForm">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="120px">
        <el-form-item label="模板名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入模板名称" />
        </el-form-item>
        <el-form-item label="模板总分" prop="templateMaxScore">
          <el-input-number v-model="form.templateMaxScore" :min="1" :max="1000" />
        </el-form-item>
        <el-form-item label="系统总分" prop="systemTotalScore">
          <el-input-number v-model="form.systemTotalScore" :min="1" :max="1000" />
        </el-form-item>
        
        <!-- 分类配置 -->
        <el-form-item label="评分分类">
          <div class="categories-config">
            <div 
              v-for="(category, categoryIndex) in form.categories" 
              :key="categoryIndex"
              class="category-item"
            >
              <div class="category-header">
                <el-input 
                  v-model="category.name" 
                  placeholder="分类名称"
                  style="width: 200px; margin-right: 12px;"
                />
                <el-input-number 
                  v-model="category.sortOrder" 
                  :min="1" 
                  placeholder="排序"
                  style="width: 100px; margin-right: 12px;"
                />
                <el-button @click="addItem(categoryIndex)" :icon="Plus" size="small">添加条目</el-button>
                <el-button @click="removeCategory(categoryIndex)" :icon="Delete" size="small" type="danger">删除分类</el-button>
              </div>
              
              <!-- 条目配置 -->
              <div class="items-config">
                <div 
                  v-for="(item, itemIndex) in category.items" 
                  :key="itemIndex"
                  class="item-row"
                >
                  <el-input 
                    v-model="item.name" 
                    placeholder="条目名称"
                    style="width: 150px; margin-right: 8px;"
                  />
                  <el-input 
                    v-model="item.description" 
                    placeholder="条目描述"
                    style="width: 200px; margin-right: 8px;"
                  />
                  <el-input-number 
                    v-model="item.maxScore" 
                    :min="0" 
                    :precision="1"
                    placeholder="最高分"
                    style="width: 100px; margin-right: 8px;"
                  />
                  <el-input-number 
                    v-model="item.weight" 
                    :min="0" 
                    :max="1"
                    :step="0.01"
                    :precision="2"
                    placeholder="权重"
                    style="width: 100px; margin-right: 8px;"
                  />
                  <el-input-number 
                    v-model="item.sortOrder" 
                    :min="1"
                    placeholder="排序"
                    style="width: 80px; margin-right: 8px;"
                  />
                  <el-button @click="removeItem(categoryIndex, itemIndex)" :icon="Delete" size="small" type="danger">删除</el-button>
                </div>
              </div>
            </div>
            
            <el-button @click="addCategory" :icon="Plus" type="primary">添加分类</el-button>
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
import { templateApi } from '../../api'

export default {
  name: 'TemplateManagement',
  components: { Plus, Edit, Check, Delete },
  setup() {
    const loading = ref(false)
    const submitting = ref(false)
    const dialogVisible = ref(false)
    const isEdit = ref(false)
    const formRef = ref(null)
    
    const templates = ref([])
    
    const form = ref({
      id: null,
      name: '',
      templateMaxScore: 100,
      systemTotalScore: 45,
      categories: []
    })
    
    const rules = {
      name: [{ required: true, message: '请输入模板名称', trigger: 'blur' }],
      templateMaxScore: [{ required: true, message: '请输入模板总分', trigger: 'blur' }],
      systemTotalScore: [{ required: true, message: '请输入系统总分', trigger: 'blur' }]
    }
    
    const dialogTitle = computed(() => isEdit.value ? '编辑模板' : '新增模板')
    
    const getTotalItems = (template) => {
      return template.categories?.reduce((total, category) => {
        return total + (category.items?.length || 0)
      }, 0) || 0
    }
    
    const loadTemplates = async () => {
      try {
        loading.value = true
        // const data = await templateApi.getList()
        // templates.value = data
        
        // 模拟数据
        const defaultTemplate = await templateApi.getDefault()
        templates.value = [defaultTemplate]
      } catch (error) {
        console.error('加载模板列表失败:', error)
        ElMessage.error('加载模板列表失败')
      } finally {
        loading.value = false
      }
    }
    
    const showAddDialog = () => {
      isEdit.value = false
      form.value = {
        id: null,
        name: '',
        templateMaxScore: 100,
        systemTotalScore: 45,
        categories: []
      }
      dialogVisible.value = true
    }
    
    const editTemplate = (template) => {
      isEdit.value = true
      form.value = JSON.parse(JSON.stringify(template))
      dialogVisible.value = true
    }
    
    const setDefault = async (template) => {
      try {
        await ElMessageBox.confirm(
          `确定要将"${template.name}"设为默认模板吗？`,
          '确认操作',
          { confirmButtonText: '确定', cancelButtonText: '取消', type: 'warning' }
        )
        
        ElMessage.success('设置成功')
        loadTemplates()
      } catch (error) {
        if (error !== 'cancel') {
          console.error('设置默认模板失败:', error)
          ElMessage.error('设置默认模板失败')
        }
      }
    }
    
    const deleteTemplate = async (template) => {
      try {
        await ElMessageBox.confirm(
          `确定要删除模板"${template.name}"吗？此操作不可恢复。`,
          '确认删除',
          { confirmButtonText: '确定删除', cancelButtonText: '取消', type: 'warning' }
        )
        
        ElMessage.success('删除成功')
        loadTemplates()
      } catch (error) {
        if (error !== 'cancel') {
          console.error('删除模板失败:', error)
          ElMessage.error('删除模板失败')
        }
      }
    }
    
    const addCategory = () => {
      form.value.categories.push({
        name: '',
        sortOrder: form.value.categories.length + 1,
        items: []
      })
    }
    
    const removeCategory = (index) => {
      form.value.categories.splice(index, 1)
    }
    
    const addItem = (categoryIndex) => {
      const category = form.value.categories[categoryIndex]
      category.items.push({
        name: '',
        description: '',
        maxScore: 10,
        weight: 0.1,
        sortOrder: category.items.length + 1
      })
    }
    
    const removeItem = (categoryIndex, itemIndex) => {
      form.value.categories[categoryIndex].items.splice(itemIndex, 1)
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
        loadTemplates()
      } catch (error) {
        console.error('保存模板失败:', error)
        ElMessage.error('保存模板失败')
      } finally {
        submitting.value = false
      }
    }
    
    const resetForm = () => {
      form.value = {
        id: null,
        name: '',
        templateMaxScore: 100,
        systemTotalScore: 45,
        categories: []
      }
      formRef.value?.resetFields()
    }
    
    onMounted(() => {
      loadTemplates()
    })
    
    return {
      loading, submitting, dialogVisible, dialogTitle, formRef, isEdit,
      templates, form, rules,
      getTotalItems, loadTemplates, showAddDialog, editTemplate, setDefault, deleteTemplate,
      addCategory, removeCategory, addItem, removeItem, submitForm, resetForm
    }
  }
}
</script>

<style scoped>
.template-management {
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

.template-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
  gap: 20px;
}

.template-card {
  transition: all 0.3s ease;
}

.template-card:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}

.template-card.is-default {
  border-color: #67c23a;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.template-name {
  font-weight: bold;
  font-size: 16px;
}

.card-actions .el-button {
  margin-left: 8px;
}

.template-info p {
  margin: 8px 0;
  color: #666;
}

.categories-preview h5 {
  margin: 16px 0 8px 0;
  color: #333;
}

.category-tag {
  margin: 4px 8px 4px 0;
}

.categories-config {
  border: 1px solid #ddd;
  border-radius: 6px;
  padding: 16px;
}

.category-item {
  margin-bottom: 20px;
  padding: 16px;
  border: 1px solid #eee;
  border-radius: 6px;
  background: #fafafa;
}

.category-header {
  display: flex;
  align-items: center;
  margin-bottom: 12px;
}

.items-config {
  margin-left: 20px;
}

.item-row {
  display: flex;
  align-items: center;
  margin-bottom: 8px;
  padding: 8px;
  background: white;
  border-radius: 4px;
}
</style>