<template>
  <div class="project-page">
    <header class="project-header">
      <div>
        <div class="project-kicker">Wiki</div>
        <h1>项目管理</h1>
        <p>管理 Wiki 项目，进入项目后编辑对应的 Wiki 树</p>
      </div>
      <button class="primary-btn" @click="openProjectModal(null)">
        <Icon icon="fluent:add-20-regular" :width="15"/>
        新增项目
      </button>
    </header>

    <section class="project-toolbar">
      <div class="search-box">
        <Icon icon="fluent:search-20-regular" :width="16"/>
        <input
            v-model="search"
            placeholder="搜索项目编码或名称"
            autocomplete="off"
            @input="handleSearchInput"
        />
      </div>
    </section>

    <section v-if="loading" class="project-state">
      <n-spin size="large"/>
    </section>

    <section v-else-if="projectList.length === 0" class="project-state">
      <div class="state-icon">
        <Icon icon="fluent:folder-open-20-regular" :width="34"/>
      </div>
      <h2>暂无项目</h2>
      <p>创建项目后即可进入 Wiki 编辑页面</p>
      <button class="primary-btn" @click="openProjectModal(null)">
        <Icon icon="fluent:add-20-regular" :width="15"/>
        新增项目
      </button>
    </section>

    <section v-else class="project-grid">
      <article v-for="project in projectList" :key="project.id" class="project-card">
        <div class="card-head">
          <div class="project-avatar">
            <Icon icon="fluent:folder-20-filled" :width="18"/>
          </div>
          <button class="open-btn" @click="openWiki(project.id)">
            进入 Wiki
            <Icon icon="fluent:chevron-right-20-regular" :width="15"/>
          </button>
        </div>
        <h2>{{ project.name }}</h2>
        <p class="project-code">{{ project.code }}</p>
        <p class="project-desc">{{ project.desc || '暂无描述' }}</p>
        <div class="card-foot">
          <span>更新于 {{ formatDate(project.updatedAt || project.createdAt) }}</span>
          <div class="card-actions">
            <button title="编辑" @click="openProjectModal(project)">
              <Icon icon="fluent:edit-20-regular" :width="14"/>
            </button>
            <button class="danger" title="删除" @click="handleDeleteProject(project)">
              <Icon icon="fluent:delete-20-regular" :width="14"/>
            </button>
          </div>
        </div>
      </article>
    </section>

    <footer v-if="totalPage > 1" class="project-pager">
      <button :disabled="pageIndex <= 1 || loading" @click="changePage(pageIndex - 1)">
        <Icon icon="fluent:chevron-left-20-regular" :width="14"/>上一页
      </button>
      <span>{{ pageIndex }} / {{ totalPage }}</span>
      <button :disabled="pageIndex >= totalPage || loading" @click="changePage(pageIndex + 1)">
        下一页<Icon icon="fluent:chevron-right-20-regular" :width="14"/>
      </button>
    </footer>
  </div>

  <n-modal v-model:show="projectModal.visible" preset="card" :title="projectModal.form.projectId ? '编辑项目' : '新增项目'" style="width: 420px;">
    <div class="project-form">
      <label>
        <span>项目编码</span>
        <n-input v-model:value="projectModal.form.code" placeholder="如 PRODUCT_DOCS"/>
      </label>
      <label>
        <span>项目名称</span>
        <n-input v-model:value="projectModal.form.name" placeholder="项目名称"/>
      </label>
      <label>
        <span>项目描述</span>
        <n-input v-model:value="projectModal.form.desc" type="textarea" placeholder="项目描述"/>
      </label>
    </div>
    <template #footer>
      <div class="modal-footer">
        <n-button @click="projectModal.visible = false">取消</n-button>
        <n-button type="primary" :loading="projectModal.saving" @click="handleSaveProject">保存</n-button>
      </div>
    </template>
  </n-modal>
</template>

<script setup lang="ts">
import {computed, onMounted, ref} from 'vue'
import {useRouter} from 'vue-router'
import {Icon} from '@iconify/vue'
import {NButton, NInput, NModal, NSpin, useDialog, useNotification} from 'naive-ui'
import dayjs from 'dayjs'
import {
  apiDeleteWikiProject,
  apiEditWikiProject,
  apiGetWikiProjectPage,
  type WikiProjectDetail,
  type EditWikiProjectParams,
  type DeleteWikiProjectParams,
  type WikiProjectPageParams,
} from '@/api/wikiProjectApi.ts'

interface WikiProjectModalState {
  visible: boolean
  saving: boolean
  form: EditWikiProjectParams
}

const router = useRouter()
const dialog = useDialog()
const notification = useNotification()

const loading = ref(false)
const projectList = ref<WikiProjectDetail[]>([])
const search = ref('')
const pageIndex = ref(1)
const pageSize = 12
const totalCount = ref(0)
let searchTimer: number | null = null

const projectModal = ref<WikiProjectModalState>({
  visible: false,
  saving: false,
  form: {
    projectId: null,
    code: '',
    name: '',
    desc: null,
  },
})

const totalPage = computed(() => Math.max(1, Math.ceil(totalCount.value / pageSize)))

const formatDate = (d: string | null) => d ? dayjs(d).format('YYYY-MM-DD HH:mm') : '-'

const loadProjectPage = () => {
  loading.value = true
  const pageParams: WikiProjectPageParams = {
    pageIndex: pageIndex.value,
    pageSize,
    search: search.value.trim() || null,
  }
  apiGetWikiProjectPage(pageParams).then(res => {
    if (res.code === 200) {
      projectList.value = res.data?.data || []
      totalCount.value = res.data?.filterCount || 0
    } else {
      projectList.value = []
      totalCount.value = 0
    }
  }).finally(() => {
    loading.value = false
  })
}

const handleSearchInput = () => {
  if (searchTimer !== null) window.clearTimeout(searchTimer)
  searchTimer = window.setTimeout(() => {
    pageIndex.value = 1
    loadProjectPage()
  }, 250)
}

const changePage = (targetPage: number) => {
  pageIndex.value = Math.min(Math.max(1, targetPage), totalPage.value)
  loadProjectPage()
}

const openWiki = (projectId: string) => {
  router.push({path: '/wiki', query: {project: projectId}})
}

const openProjectModal = (project: WikiProjectDetail | null) => {
  const form: EditWikiProjectParams = project
      ? {
        projectId: project.id,
        code: project.code,
        name: project.name,
        desc: project.desc || '',
      }
      : {
        projectId: null,
        code: '',
        name: '',
        desc: '',
      }
  projectModal.value.form = form
  projectModal.value.visible = true
}

const handleSaveProject = () => {
  if (!projectModal.value.form.code.trim() || !projectModal.value.form.name.trim()) {
    notification.warning({title: '请输入项目编码和名称', duration: 2000})
    return
  }
  projectModal.value.saving = true
  apiEditWikiProject(projectModal.value.form).then(res => {
    if (res.code === 200) {
      notification.success({title: '保存成功', duration: 2000})
      projectModal.value.visible = false
      loadProjectPage()
    } else {
      notification.error({title: '保存失败', content: res.message, duration: 3000})
    }
  }).finally(() => {
    projectModal.value.saving = false
  })
}

const handleDeleteProject = (project: WikiProjectDetail) => {
  dialog.warning({
    title: '删除确认',
    content: `确定删除项目「${project.name}」吗？`,
    positiveText: '确定删除',
    negativeText: '取消',
    onPositiveClick: () => {
      const deleteParams: DeleteWikiProjectParams = {projectId: project.id}
      apiDeleteWikiProject(deleteParams).then(res => {
        if (res.code === 200) {
          notification.success({title: '已删除', duration: 2000})
          loadProjectPage()
        } else {
          notification.error({title: '删除失败', content: res.message, duration: 3000})
        }
      })
    },
  })
}

onMounted(loadProjectPage)
</script>

<style scoped lang="scss">
/* 与 wiki 编辑页同款：灰底 + 紫蓝 #4f46e5 强调 */
.project-page {
  min-height: calc(100vh - 28px);
  padding: 24px 28px 40px;
  background: #f5f7fa;
  color: #1f2937;
  font-size: 13px;
}

.project-header {
  max-width: 1200px;
  margin: 0 auto 18px;
  padding: 22px 26px;
  background: #fff;
  border: 1px solid #e8eaf0;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
}

.project-header > div:first-child {
  display: flex;
  align-items: center;
  gap: 14px;
  min-width: 0;
}

.project-kicker {
  display: inline-flex;
  align-items: center;
  height: 32px;
  padding: 0 10px;
  border-radius: 8px;
  background: linear-gradient(135deg, #eef2ff 0%, #e0e7ff 100%);
  color: #4f46e5;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: .5px;
  text-transform: uppercase;
  flex-shrink: 0;
}

.project-header > div:first-child > div {
  min-width: 0;
}

.project-header h1 {
  display: inline;
  margin: 0;
  font-size: 22px;
  line-height: 1.2;
  font-weight: 700;
  color: #111827;
  letter-spacing: -.3px;
}

.project-header p {
  margin: 4px 0 0;
  color: #9ca3af;
  font-size: 12px;
}

.primary-btn {
  height: 32px;
  padding: 0 14px;
  border: 1px solid #4f46e5;
  border-radius: 8px;
  background: #4f46e5;
  color: #fff;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  box-shadow: 0 1px 2px rgba(79, 70, 229, .25);
  transition: all .12s;
  flex-shrink: 0;

  &:hover { background: #4338ca; border-color: #4338ca; }
}

.open-btn {
  height: 30px;
  padding: 0 12px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  background: #fff;
  color: #4b5563;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 5px;
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  transition: all .12s;

  &:hover {
    background: #eef2ff;
    color: #4f46e5;
    border-color: #c7d2fe;
  }
}

.project-toolbar {
  max-width: 1200px;
  margin: 0 auto 16px;
}

.search-box {
  width: min(420px, 100%);
  height: 36px;
  padding: 0 12px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  background: #fff;
  color: #9ca3af;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all .12s;

  &:focus-within {
    border-color: #c7d2fe;
    box-shadow: 0 0 0 3px rgba(79, 70, 229, .12);
  }
}

.search-box input {
  flex: 1;
  min-width: 0;
  border: 0;
  outline: none;
  background: transparent;
  color: #1f2937;
  font-size: 13px;
}

.search-box input::placeholder { color: #9ca3af; }

.project-grid {
  max-width: 1200px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 14px;
}

.project-card {
  min-height: 200px;
  padding: 18px;
  border: 1px solid #e8eaf0;
  border-radius: 12px;
  background: #fff;
  transition: border-color .12s, box-shadow .12s, transform .12s;
}

.project-card:hover {
  border-color: #c7d2fe;
  box-shadow: 0 12px 32px rgba(15, 23, 42, .08);
  transform: translateY(-1px);
}

.card-head,
.card-foot {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.project-avatar {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  background: linear-gradient(135deg, #eef2ff 0%, #e0e7ff 100%);
  color: #4f46e5;
  display: flex;
  align-items: center;
  justify-content: center;
}

.project-card h2 {
  margin: 18px 0 5px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-size: 16px;
  font-weight: 700;
  color: #111827;
  letter-spacing: -.2px;
}

.project-code {
  display: inline-block;
  margin: 0 0 10px;
  padding: 2px 8px;
  border-radius: 5px;
  background: #eef2ff;
  color: #4f46e5;
  font-size: 11px;
  font-weight: 600;
  font-family: ui-monospace, monospace;
  font-feature-settings: "tnum";
}

.project-desc {
  min-height: 40px;
  margin: 0;
  color: #6b7280;
  font-size: 13px;
  line-height: 1.6;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-foot {
  margin-top: 18px;
  padding-top: 12px;
  border-top: 1px solid #f1f3f7;
  color: #9ca3af;
  font-size: 12px;
  font-feature-settings: "tnum";
}

.card-actions {
  display: inline-flex;
  gap: 6px;
}

.card-actions button {
  width: 28px;
  height: 28px;
  border: 1px solid #e5e7eb;
  border-radius: 7px;
  background: #fff;
  color: #6b7280;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all .12s;
}

.card-actions button:hover {
  background: #eef2ff;
  border-color: #c7d2fe;
  color: #4f46e5;
}

.card-actions .danger:hover {
  background: #fef2f2;
  border-color: #fecaca;
  color: #dc2626;
}

.project-state {
  max-width: 1200px;
  min-height: 360px;
  margin: 0 auto;
  padding: 60px 32px;
  background: #fff;
  border: 1px solid #e8eaf0;
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
}

.state-icon {
  width: 72px;
  height: 72px;
  border-radius: 50%;
  background: linear-gradient(135deg, #eef2ff 0%, #e0e7ff 100%);
  color: #4f46e5;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 14px;
}

.project-state h2 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #111827;
  letter-spacing: -.1px;
}

.project-state p {
  margin: 4px 0 16px;
  color: #9ca3af;
  font-size: 13px;
}

.project-pager {
  max-width: 1200px;
  margin: 20px auto 0;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 14px;
  color: #9ca3af;
  font-size: 12px;
  font-feature-settings: "tnum";
}

.project-pager button {
  height: 30px;
  padding: 0 13px;
  border: 1px solid #e5e7eb;
  border-radius: 7px;
  background: #fff;
  color: #4b5563;
  display: inline-flex;
  align-items: center;
  gap: 5px;
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  transition: all .12s;
}

.project-pager button:hover:not(:disabled) {
  background: #eef2ff;
  color: #4f46e5;
  border-color: #c7d2fe;
}

.project-pager button:disabled {
  opacity: .45;
  cursor: not-allowed;
}

.project-form {
  display: grid;
  gap: 14px;

  :deep(.n-input) {
    border-radius: 8px;
  }
}

.project-form label {
  display: grid;
  gap: 6px;
}

.project-form span {
  color: #4b5563;
  font-size: 12px;
  font-weight: 600;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
}

@media (max-width: 1080px) {
  .project-page { padding: 20px 20px 36px; }
  .project-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 720px) {
  .project-page { padding: 16px 14px 32px; }

  .project-header {
    flex-direction: column;
    align-items: flex-start;
    padding: 18px 18px;
  }

  .project-header > div:first-child { gap: 12px; }

  .project-header h1 { font-size: 20px; }

  .project-header .primary-btn {
    align-self: stretch;
    justify-content: center;
  }

  .project-grid {
    grid-template-columns: 1fr;
  }

  .card-foot {
    display: block;
  }

  .card-actions {
    margin-top: 10px;
  }
}
</style>
