<template>
  <div class="wiki-page">
    <!-- 左侧：页面树 -->
    <div class="wiki-sidebar">
      <div class="sidebar-header">
        <button class="back-btn" @click="router.push('/wiki-project')" title="返回项目管理">
          <Icon icon="fluent:arrow-left-20-regular" :width="15"/>
        </button>
        <div class="sidebar-icon">
          <Icon icon="fluent:book-20-filled" :width="16"/>
        </div>
        <div class="sidebar-title">
          <div class="sidebar-title-main">Wiki</div>
          <div class="sidebar-title-sub">知识库</div>
        </div>
        <button class="sidebar-add" title="新建页面" @click="handleNewPage(null)">
          <Icon icon="fluent:add-16-regular" :width="14"/>
        </button>
      </div>

      <div class="project-context">
        <button class="project-back" @click="router.push('/wiki-project')">
          <Icon icon="fluent:folder-20-regular" :width="14"/>
          项目管理
        </button>
        <div class="project-current">
          <span>{{ currentProject?.name || '未选择项目' }}</span>
          <small>{{ currentProject?.code || '-' }}</small>
        </div>
      </div>

      <div class="sidebar-tree">
        <div v-if="treeLoading" class="flex justify-center py-6">
          <n-spin size="small"/>
        </div>
        <div v-else-if="pageTree.length === 0" class="empty-tree">
          <Icon icon="fluent:document-add-20-regular" :width="32" class="empty-tree-icon"/>
          <p>暂无页面</p>
          <button class="sidebar-empty-btn" @click="handleNewPage(null)">
            <Icon icon="fluent:add-16-regular" :width="13"/>创建第一个页面
          </button>
        </div>
        <template v-else>
          <WikiTreeNode
              v-for="node in pageTree"
              :key="node.id"
              :node="node"
              :active-id="currentPageId"
              @select="handleSelectPage"
              @add-child="handleNewPage"
              @contextmenu="handleNodeContextMenu"
          />
        </template>
      </div>
    </div>

    <!-- 右侧：内容区 -->
    <div class="wiki-main">
      <!-- 无页面时的空状态 -->
      <div v-if="!currentPageId && !isCreating" class="wiki-empty">
        <div class="wiki-empty-icon">
          <Icon icon="fluent:book-open-20-regular" :width="40"/>
        </div>
        <h2 class="wiki-empty-title">开始编写知识库</h2>
        <p class="wiki-empty-desc">选择左侧已有页面，或创建新页面开始编辑</p>
        <button class="wiki-primary-btn" @click="handleNewPage(null)">
          <Icon icon="fluent:add-20-regular" :width="15"/>新建页面
        </button>
      </div>

      <!-- 编辑模式 -->
      <div v-else-if="isEditing || isCreating" class="wiki-editor-view">
        <div class="editor-header">
          <n-input
              v-model:value="editForm.title"
              placeholder="页面标题"
              size="large"
              class="title-input"
          />
          <button class="wiki-ghost-btn" @click="handleCancelEdit">取消</button>
          <button class="wiki-primary-btn" :disabled="saving" @click="handleSave">
            <Icon icon="fluent:save-20-regular" :width="14"/>{{ saving ? '保存中…' : '保存' }}
          </button>
        </div>
        <div class="editor-wrap">
          <RichEditor v-model="editForm.content"/>
        </div>
      </div>

      <!-- 查看模式 -->
      <div v-else-if="currentPage" class="wiki-view">
        <div class="view-header">
          <div class="view-header-text">
            <h1 class="page-title">{{ currentPage.title }}</h1>
            <div class="page-meta">
              <Icon icon="fluent:clock-20-regular" :width="12"/>
              <span>更新于 {{ formatDate(currentPage.updatedAt) }}</span>
            </div>
          </div>
          <div class="view-header-actions">
            <button class="wiki-ghost-btn" @click="handleNewPage(currentPage.id)">
              <Icon icon="fluent:add-20-regular" :width="13"/>子页面
            </button>
            <button class="wiki-primary-btn" @click="handleEdit">
              <Icon icon="fluent:edit-20-regular" :width="13"/>编辑
            </button>
            <button class="wiki-danger-btn" title="删除" @click="handleDelete">
              <Icon icon="fluent:delete-20-regular" :width="13"/>
            </button>
          </div>
        </div>

        <!-- 可滚动内容区 -->
        <div class="view-scroll-body">
          <!-- 正文 -->
          <RichContentViewer :content="currentPage.content || '<p>暂无内容</p>'" class="view-content prose"/>

          <!-- 附件 -->
          <div class="view-section">
            <div class="section-title">
              <Icon icon="fluent:attach-20-regular" :width="14"/>
              <span>附件</span>
              <span v-if="fileList.length" class="section-count">{{ fileList.length }}</span>
              <button class="section-action" @click="fileInputRef?.click()">
                <Icon icon="fluent:add-16-regular" :width="13"/>上传
              </button>
            </div>
            <div v-if="fileList.length === 0" class="section-empty">暂无附件</div>
            <div v-else class="file-list">
              <div v-for="f in fileList" :key="f.id" class="file-item">
                <Icon icon="fluent:document-20-regular" :width="16" class="file-icon"/>
                <button class="file-name" @click="handlePreviewFile(f)">{{ f.fileName }}</button>
                <span class="file-size">{{ formatFileSize(f.fileSize) }}</span>
                <button class="file-action" title="下载" @click="handleDownloadFile(f)">
                  <Icon icon="fluent:arrow-download-20-regular" :width="13"/>
                </button>
                <button class="file-action file-action--del" title="删除" @click="handleDeleteFile(f)">
                  <Icon icon="fluent:dismiss-16-regular" :width="11"/>
                </button>
              </div>
            </div>
          </div>

          <!-- 历史版本 -->
          <div class="view-section">
            <div class="section-title">
              <Icon icon="fluent:history-20-regular" :width="14"/>
              <span>历史版本</span>
              <span v-if="historyVisible && historyList.length" class="section-count">{{ historyList.length }}</span>
              <button class="section-action" @click="historyVisible = !historyVisible">
                <Icon :icon="historyVisible ? 'fluent:chevron-up-16-regular' : 'fluent:chevron-down-16-regular'" :width="13"/>
                {{ historyVisible ? '收起' : '展开' }}
              </button>
            </div>
            <template v-if="historyVisible">
              <div v-if="historyList.length === 0" class="section-empty">暂无历史</div>
              <div v-else class="history-list">
                <div v-for="h in historyList" :key="h.id" class="history-item">
                  <span class="history-version">v{{ h.versionNo }}</span>
                  <span class="history-editor">{{ h.editorName || '-' }}</span>
                  <span class="history-date">{{ formatDate(h.createdAt) }}</span>
                </div>
              </div>
            </template>
          </div>
        </div>
      </div>

      <div v-else-if="pageLoading" class="wiki-empty">
        <n-spin/>
      </div>
    </div>

    <input type="file" ref="fileInputRef" style="display:none" @change="handleFileUpload"/>
  </div>

  <!-- 右键菜单 -->
  <div
      v-if="contextMenu.visible"
      class="wiki-context-menu"
      :style="{ top: contextMenu.y + 'px', left: contextMenu.x + 'px' }"
      @mouseleave="contextMenu.visible = false"
  >
    <button class="ctx-item" @click="openVisibilityModal">
      <Icon icon="fluent:globe-20-regular" :width="15"/>
      设置可见性
    </button>
    <button
        v-if="contextMenu.node?.isPublic"
        class="ctx-item"
        @click="copyPublicLink"
    >
      <Icon icon="fluent:link-20-regular" :width="15"/>
      复制分享链接
    </button>
  </div>

  <!-- 可见性设置弹窗 -->
  <n-modal v-model:show="visibilityModal.visible" preset="card" title="设置可见性" style="width: 420px;">
    <div class="visibility-form">
      <div class="visibility-row">
        <div>
          <div class="visibility-label">公开此页面</div>
          <div class="visibility-hint">开启后可通过链接访问</div>
        </div>
        <n-switch v-model:value="visibilityModal.isPublic" />
      </div>
      <div v-if="visibilityModal.isPublic" class="visibility-row">
        <div>
          <div class="visibility-label">授权码访问</div>
          <div class="visibility-hint">开启后需输入授权码访问</div>
        </div>
        <n-switch v-model:value="visibilityModal.requireAuth" />
      </div>
      <div v-if="visibilityModal.isPublic && visibilityModal.requireAuth" class="visibility-code">
        <span class="visibility-url-label">授权码</span>
        <n-input
            v-model:value="visibilityModal.accessCode"
            placeholder="已有授权码时可留空不变"
            autocomplete="off"
            autocapitalize="off"
            autocorrect="off"
            spellcheck="false"
        />
      </div>
      <div v-if="visibilityModal.isPublic" class="visibility-url">
        <span class="visibility-url-label">公开链接</span>
        <span class="visibility-url-text">{{ publicUrl }}</span>
      </div>
    </div>
    <template #footer>
      <div class="flex justify-end gap-2">
        <n-button @click="visibilityModal.visible = false">取消</n-button>
        <n-button type="primary" :loading="visibilityModal.saving" @click="handleSaveVisibility">保存</n-button>
      </div>
    </template>
  </n-modal>

  <FilePreviewModal v-model:show="previewVisible" :file="previewFile" />
</template>

<script setup lang="ts">
import {ref, computed, watch, onMounted, defineComponent, h} from 'vue'
import {useRoute, useRouter} from 'vue-router'
import {Icon} from '@iconify/vue'
import {NButton, NInput, NSpin, NSwitch, NModal, useNotification, useDialog} from 'naive-ui'
import dayjs from 'dayjs'
import RichEditor from '@/components/wiki/RichEditor.vue'
import FilePreviewModal, { type PreviewFile } from '@/components/common/FilePreviewModal.vue'
import RichContentViewer from '@/components/common/RichContentViewer.vue'
import {
  apiGetWikiPageTree,
  apiGetWikiPageDetail,
  apiEditWikiPage,
  apiDeleteWikiPage,
  apiGetWikiPageFileList,
  apiSaveWikiPageFile,
  apiDeleteWikiPageFile,
  apiGetWikiPageHistoryList,
  apiSetWikiPageVisibility,
  type WikiPageTreeItem,
  type WikiPageDetail,
  type WikiPageFileDetail,
  type WikiPageHistoryItem,
  type EditWikiPageParams,
  type SetWikiPageVisibilityParams,
} from '@/api/wikiApi.ts'
import {apiUploadFile} from '@/api/storageApi.ts'
import {downloadFromUrl} from '@/utils/file.ts'
import {
  apiGetWikiProjectDetail,
  type WikiProjectDetail,
} from '@/api/wikiProjectApi.ts'

// 树节点组件
interface TreeContextMenuPayload {
  node: WikiPageTreeItem
  event: MouseEvent
}

interface TreeContextMenuState {
  visible: boolean
  x: number
  y: number
  node: WikiPageTreeItem | null
}

interface WikiPageEditForm {
  title: string
  content: string | null
  parentId: string | null
}

interface WikiVisibilityModalState {
  visible: boolean
  isPublic: boolean
  requireAuth: boolean
  accessCode: string
  saving: boolean
}

const WikiTreeNode = defineComponent({
  name: 'WikiTreeNode',
  props: {
    node: {type: Object as () => WikiPageTreeItem, required: true},
    activeId: {type: String, default: null},
    depth: {type: Number, default: 0},
  },
  emits: ['select', 'add-child', 'contextmenu'],
  setup(props, {emit}) {
    const expanded = ref(true)
    return () => {
      const {node, activeId, depth} = props
      const isActive = node.id === activeId
      const publicIcon = node.isPublic
          ? h(Icon, {icon: 'fluent:globe-20-regular', width: 12, class: node.requireAuth ? 'text-blue-400' : 'text-green-500', title: node.requireAuth ? '授权码访问' : '公开访问'})
          : null
      return h('div', {class: 'tree-node'}, [
        h('div', {
          class: ['tree-node-row', isActive && 'active'],
          style: {paddingLeft: `${12 + depth * 16}px`},
          onClick: () => emit('select', node.id),
          onContextmenu: (e: MouseEvent) => {e.preventDefault(); emit('contextmenu', {node, event: e})}
        }, [
          node.childList?.length
              ? h('span', {
                class: 'tree-expand',
                onClick: (e: Event) => {e.stopPropagation(); expanded.value = !expanded.value}
              }, h(Icon, {icon: expanded.value ? 'fluent:chevron-down-16-regular' : 'fluent:chevron-right-16-regular', width: 12}))
              : h('span', {class: 'tree-expand-placeholder'}),
          h(Icon, {icon: 'fluent:document-20-regular', width: 14, class: 'text-gray-400 flex-shrink-0'}),
          h('span', {class: 'tree-node-title'}, node.title),
          publicIcon,
          h('span', {
            class: 'tree-node-add',
            onClick: (e: Event) => {e.stopPropagation(); emit('add-child', node.id)}
          }, h(Icon, {icon: 'fluent:add-16-regular', width: 12})),
        ]),
        expanded.value && node.childList?.length
            ? h('div', node.childList.map(child =>
                h(WikiTreeNode, {
                  node: child, activeId, depth: depth + 1,
                  onSelect: (id: string) => emit('select', id),
                  onAddChild: (id: string) => emit('add-child', id),
                  onContextmenu: (payload: TreeContextMenuPayload) => emit('contextmenu', payload),
                })
            ))
            : null,
      ])
    }
  }
})

const route = useRoute()
const router = useRouter()
const notification = useNotification()
const dialog = useDialog()

const currentPageId = computed(() => route.query.page as string | undefined)
const currentProjectId = ref((route.query.project as string | undefined) || '')
const projectId = computed(() => currentProjectId.value)

const treeLoading = ref(false)
const pageLoading = ref(false)
const saving = ref(false)
const isEditing = ref(false)
const isCreating = ref(false)
const historyVisible = ref(false)

const currentProject = ref<WikiProjectDetail | null>(null)
const pageTree = ref<WikiPageTreeItem[]>([])
const currentPage = ref<WikiPageDetail | null>(null)
const fileList = ref<WikiPageFileDetail[]>([])
const historyList = ref<WikiPageHistoryItem[]>([])
const fileInputRef = ref<HTMLInputElement>()

const editForm = ref<WikiPageEditForm>({
  title: '',
  content: null,
  parentId: null,
})

const previewVisible = ref(false)
const previewFile = ref<PreviewFile | null>(null)

const handlePreviewFile = (f: WikiPageFileDetail) => {
  previewFile.value = { url: f.url, fileName: f.fileName }
  previewVisible.value = true
}

const handleDownloadFile = (f: WikiPageFileDetail) => {
  downloadFromUrl(f.url, f.fileName)
}

// 右键菜单
const contextMenu = ref<TreeContextMenuState>({
  visible: false, x: 0, y: 0, node: null,
})

const handleNodeContextMenu = ({ node, event }: TreeContextMenuPayload) => {
  contextMenu.value = { visible: true, x: event.clientX, y: event.clientY, node }
}

// 可见性弹窗
const visibilityModal = ref<WikiVisibilityModalState>({
  visible: false,
  isPublic: false,
  requireAuth: false,
  accessCode: '',
  saving: false,
})

const publicUrl = computed(() => {
  if (!contextMenu.value.node) return ''
  return `${window.location.origin}/public-wiki/${projectId.value}?page=${contextMenu.value.node.id}`
})

const openVisibilityModal = () => {
  const node = contextMenu.value.node
  if (!node) return
  visibilityModal.value = {
    visible: true,
    isPublic: node.isPublic,
    requireAuth: node.requireAuth,
    accessCode: node.accessCode || '',
    saving: false,
  }
  contextMenu.value.visible = false
}

const copyPublicLink = () => {
  const node = contextMenu.value.node
  if (!node) return
  navigator.clipboard.writeText(publicUrl.value)
  notification.success({ title: '链接已复制', duration: 2000 })
  contextMenu.value.visible = false
}

const handleSaveVisibility = () => {
  const node = contextMenu.value.node
  if (!node) return
  if (visibilityModal.value.isPublic && visibilityModal.value.requireAuth && !visibilityModal.value.accessCode.trim() && !node.requireAuth) {
    notification.warning({ title: '请输入授权码', duration: 2000 })
    return
  }
  visibilityModal.value.saving = true
  const visibilityParams: SetWikiPageVisibilityParams = {
    pageId: node.id,
    isPublic: visibilityModal.value.isPublic,
    requireAuth: visibilityModal.value.isPublic ? visibilityModal.value.requireAuth : false,
    accessCode: visibilityModal.value.isPublic && visibilityModal.value.requireAuth ? visibilityModal.value.accessCode : null,
  }
  apiSetWikiPageVisibility(visibilityParams).then(res => {
    if (res.code === 200) {
      notification.success({ title: '保存成功', duration: 2000 })
      visibilityModal.value.visible = false
      loadTree()
    } else {
      notification.error({ title: '保存失败', content: res.message, duration: 3000 })
    }
  }).catch(err => {
    notification.error({ title: '保存失败', content: err?.message || '网络错误', duration: 3000 })
  }).finally(() => {
    visibilityModal.value.saving = false
  })
}

const loadProjectDetail = (targetProjectId: string) => {
  apiGetWikiProjectDetail(targetProjectId).then(res => {
    if (res.code === 200) {
      currentProject.value = res.data
    } else {
      notification.error({title: '项目不存在', content: res.message, duration: 3000})
      router.replace('/wiki-project')
    }
  }).catch(() => {
    notification.error({title: '项目不存在', duration: 3000})
    router.replace('/wiki-project')
  })
}

const loadTree = () => {
  if (!projectId.value) return
  treeLoading.value = true
  apiGetWikiPageTree({projectId: projectId.value}).then(res => {
    if (res.code === 200) pageTree.value = res.data
  }).finally(() => {treeLoading.value = false})
}

const loadPage = (pageId: string) => {
  pageLoading.value = true
  isEditing.value = false
  isCreating.value = false
  currentPage.value = null
  fileList.value = []
  historyList.value = []
  historyVisible.value = false
  apiGetWikiPageDetail(pageId).then(res => {
    if (res.code === 200) {
      currentPage.value = res.data
      loadFiles(pageId)
    }
  }).finally(() => {pageLoading.value = false})
}

const loadFiles = (pageId: string) => {
  apiGetWikiPageFileList({pageId}).then(res => {
    if (res.code === 200) fileList.value = res.data
  })
}

const loadHistory = (pageId: string) => {
  apiGetWikiPageHistoryList({pageId}).then(res => {
    if (res.code === 200) historyList.value = res.data
  })
}

watch(historyVisible, (val) => {
  if (val && currentPageId.value && historyList.value.length === 0) {
    loadHistory(currentPageId.value)
  }
})

const handleSelectPage = (pageId: string) => {
  router.push({path: '/wiki', query: {project: projectId.value, page: pageId}})
}

const handleNewPage = (parentId: string | null) => {
  isCreating.value = true
  isEditing.value = false
  editForm.value = {title: '', content: null, parentId}
  router.push({path: '/wiki', query: {project: projectId.value}})
}

const handleEdit = () => {
  if (!currentPage.value) return
  isEditing.value = true
  editForm.value = {
    title: currentPage.value.title,
    content: currentPage.value.content,
    parentId: currentPage.value.parentId,
  }
}

const handleCancelEdit = () => {
  isEditing.value = false
  isCreating.value = false
}

const handleSave = () => {
  if (!editForm.value.title.trim()) {
    notification.warning({title: '请输入页面标题', duration: 2000})
    return
  }
  saving.value = true
  const params: EditWikiPageParams = {
    pageId: isCreating.value ? null : (currentPageId.value || null),
    projectId: projectId.value,
    parentId: editForm.value.parentId,
    title: editForm.value.title,
    content: editForm.value.content,
    seq: 0,
    isPublic: currentPage.value?.isPublic || false,
    requireAuth: currentPage.value?.requireAuth || false,
    accessCode: currentPage.value?.accessCode || null,
  }
  apiEditWikiPage(params).then(res => {
    if (res.code === 200) {
      notification.success({title: '保存成功', duration: 2000})
      loadTree()
      router.push({path: '/wiki', query: {project: projectId.value, page: res.data}})
    } else {
      notification.error({title: '保存失败', content: res.message, duration: 3000})
    }
  }).catch(err => {
    notification.error({title: '保存失败', content: `${err.message || err}`, duration: 3000})
  }).finally(() => {saving.value = false})
}

const handleDelete = () => {
  if (!currentPage.value) return
  dialog.warning({
    title: '删除确认',
    content: `确定要删除页面「${currentPage.value.title}」吗？`,
    positiveText: '确定删除',
    negativeText: '取消',
    onPositiveClick: () => {
      apiDeleteWikiPage({pageId: currentPage.value!.id}).then(res => {
        if (res.code === 200) {
          notification.success({title: '已删除', duration: 2000})
          loadTree()
          router.push({path: '/wiki', query: {project: projectId.value}})
        } else {
          notification.error({title: '删除失败', content: res.message, duration: 3000})
        }
      })
    }
  })
}

const handleFileUpload = (e: Event) => {
  const file = (e.target as HTMLInputElement).files?.[0]
  if (!file || !currentPage.value) return
  apiUploadFile({file, fileName: file.name, fileSize: file.size}).then(res => {
    if (res.code === 200 && res.data) {
      apiSaveWikiPageFile({
        pageId: currentPage.value!.id,
        fileInfoId: res.data.fileInfoId,
        fileName: res.data.fileName,
        fileType: res.data.type,
        fileSize: res.data.fileSize,
        bucketName: res.data.bucketName,
        objectName: res.data.objectName,
        fileObjectName: res.data.fileObjectName,
        fileHash: null,
        url: res.data.url,
      }).then(r => {
        if (r.code === 200) {
          notification.success({title: '上传成功', duration: 2000})
          loadFiles(currentPage.value!.id)
        }
      })
    }
  })
  ;(e.target as HTMLInputElement).value = ''
}

const handleDeleteFile = (f: WikiPageFileDetail) => {
  dialog.warning({
    title: '删除确认',
    content: `确定删除附件「${f.fileName}」吗？`,
    positiveText: '确定',
    negativeText: '取消',
    onPositiveClick: () => {
      apiDeleteWikiPageFile({fileId: f.id}).then(res => {
        if (res.code === 200) {
          loadFiles(currentPage.value!.id)
        }
      })
    }
  })
}

const formatDate = (d: string | null) => d ? dayjs(d).format('YYYY-MM-DD HH:mm') : '-'

const formatFileSize = (size: number | null) => {
  if (!size) return '-'
  if (size < 1024) return `${size}B`
  if (size < 1024 * 1024) return `${(size / 1024).toFixed(1)}KB`
  return `${(size / 1024 / 1024).toFixed(1)}MB`
}

watch(() => currentPageId.value, (id) => {
  if (projectId.value && id && id !== 'null' && id !== 'undefined') loadPage(id)
}, {immediate: true})

watch(() => projectId.value, (id) => {
  if (!id) {
    router.replace('/wiki-project')
    return
  }
  loadProjectDetail(id)
  loadTree()
}, {immediate: true})

watch(() => route.query.project, (routeProjectId) => {
  if (typeof routeProjectId === 'string' && routeProjectId && routeProjectId !== currentProjectId.value) {
    currentProjectId.value = routeProjectId
    pageTree.value = []
    currentPage.value = null
    fileList.value = []
    isCreating.value = false
    isEditing.value = false
  }
})

onMounted(() => {
  if (!currentPageId.value) {
    isCreating.value = false
    isEditing.value = false
  }
})
</script>

<style scoped lang="scss">
.wiki-page {
  display: flex;
  gap: 12px;
  height: calc(100vh - 28px);
  overflow: hidden;
  background: #f5f7fa;
  font-size: 13px;
}

/* ══ 左侧树 ════════════════════════════════════════════ */
.wiki-sidebar {
  width: 260px;
  flex-shrink: 0;
  background: #fff;
  border: 1px solid #e8eaf0;
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.sidebar-header {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 12px;
  border-bottom: 1px solid #f1f3f7;
}

.project-context {
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 10px 12px;
  border-bottom: 1px solid #f1f3f7;
  background: #fafbfc;
}

.project-back {
  height: 30px;
  padding: 0 10px;
  border: 1px solid #e5e7eb;
  border-radius: 7px;
  background: #fff;
  color: #6b7280;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all .12s;

  &:hover {
    background: #eef2ff;
    color: #4f46e5;
    border-color: #c7d2fe;
  }

}

.project-current {
  min-width: 0;
  padding: 8px 10px;
  border-radius: 8px;
  background: #fff;
  border: 1px solid #eef1f6;
}

.project-current span,
.project-current small {
  display: block;
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.project-current span {
  color: #111827;
  font-size: 13px;
  font-weight: 650;
}

.project-current small {
  margin-top: 2px;
  color: #9ca3af;
  font-size: 11px;
}

.back-btn {
  width: 28px; height: 28px;
  border: 1px solid #e5e7eb;
  border-radius: 7px;
  background: #fff;
  color: #6b7280;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  flex-shrink: 0;
  transition: all .12s;
  &:hover { background: #f9fafb; color: #1f2937; border-color: #d1d5db; }
}

.sidebar-icon {
  flex-shrink: 0;
  width: 32px; height: 32px;
  border-radius: 8px;
  background: linear-gradient(135deg, #eef2ff 0%, #e0e7ff 100%);
  color: #4f46e5;
  display: flex; align-items: center; justify-content: center;
}

.sidebar-title {
  flex: 1;
  min-width: 0;
}

.sidebar-title-main {
  font-size: 13px;
  font-weight: 600;
  color: #111827;
  letter-spacing: -.1px;
  line-height: 1.2;
}

.sidebar-title-sub {
  font-size: 11px;
  color: #9ca3af;
  margin-top: 1px;
}

.sidebar-add {
  flex-shrink: 0;
  width: 28px; height: 28px;
  border: none;
  border-radius: 7px;
  background: #4f46e5;
  color: #fff;
  display: flex; align-items: center; justify-content: center;
  cursor: pointer;
  box-shadow: 0 1px 2px rgba(79,70,229,.25);
  transition: background .12s;
  &:hover { background: #4338ca; }
}

.sidebar-tree {
  flex: 1;
  overflow-y: auto;
  padding: 6px 0;

  &::-webkit-scrollbar { width: 4px; }
  &::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 2px; }
  &::-webkit-scrollbar-track { background: transparent; }
}

.empty-tree {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 32px 16px;
  gap: 8px;
  color: #9ca3af;
  font-size: 12px;

  p { margin: 0; }
}

.empty-tree-icon { color: #d1d5db; margin-bottom: 4px; }

.sidebar-empty-btn {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  height: 28px;
  padding: 0 12px;
  border-radius: 7px;
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  background: #4f46e5;
  border: 1px solid #4f46e5;
  color: #fff;
  margin-top: 4px;
  &:hover { background: #4338ca; border-color: #4338ca; }
}

:deep(.tree-node-row) {
  display: flex;
  align-items: center;
  gap: 5px;
  padding: 6px 10px;
  cursor: pointer;
  border-radius: 6px;
  margin: 1px 8px;
  font-size: 13px;
  color: #374151;
  transition: background .12s;

  &:hover {
    background: #f3f4f6;
    .tree-node-add { opacity: 1; }
  }

  &.active {
    background: #eef2ff;
    color: #4f46e5;
    font-weight: 500;
  }
}

:deep(.tree-expand) {
  width: 16px;
  height: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  color: #9ca3af;
  border-radius: 4px;
  &:hover { color: #4f46e5; background: rgba(79,70,229,.08); }
}

:deep(.tree-expand-placeholder) {
  width: 16px;
  flex-shrink: 0;
}

:deep(.tree-node-title) {
  flex: 1;
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

:deep(.tree-node-add) {
  width: 18px;
  height: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  color: #9ca3af;
  border-radius: 4px;
  flex-shrink: 0;
  transition: opacity .12s, all .12s;
  &:hover { background: #e0e7ff; color: #4f46e5; }
}

/* ══ 右侧 ══════════════════════════════════════════════ */
.wiki-main {
  flex: 1;
  min-width: 0;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  background: #fff;
  border: 1px solid #e8eaf0;
  border-radius: 12px;
}

/* 空状态 */
.wiki-empty {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 32px;
  gap: 4px;
}

.wiki-empty-icon {
  width: 72px; height: 72px;
  border-radius: 50%;
  background: linear-gradient(135deg, #eef2ff 0%, #e0e7ff 100%);
  color: #4f46e5;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 12px;
}

.wiki-empty-title {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #111827;
  letter-spacing: -.1px;
}

.wiki-empty-desc {
  margin: 4px 0 16px;
  font-size: 13px;
  color: #9ca3af;
}

/* 通用按钮 */
.wiki-primary-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  height: 32px;
  padding: 0 14px;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  background: #4f46e5;
  border: 1px solid #4f46e5;
  color: #fff;
  box-shadow: 0 1px 2px rgba(79,70,229,.25);
  transition: all .12s;
  &:hover:not(:disabled) { background: #4338ca; border-color: #4338ca; }
  &:disabled { opacity: .5; cursor: not-allowed; box-shadow: none; }
}

.wiki-ghost-btn {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  height: 32px;
  padding: 0 12px;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  background: #fff;
  border: 1px solid #e5e7eb;
  color: #4b5563;
  transition: all .12s;
  &:hover { background: #f9fafb; color: #1f2937; border-color: #d1d5db; }
}

.wiki-danger-btn {
  width: 32px;
  height: 32px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  cursor: pointer;
  background: #fff;
  border: 1px solid #e5e7eb;
  color: #6b7280;
  transition: all .12s;
  &:hover { background: #fef2f2; color: #dc2626; border-color: #fecaca; }
}

/* 编辑模式 */
.wiki-editor-view {
  display: flex;
  flex-direction: column;
  height: 100%;
  padding: 16px 20px;
  gap: 12px;
}

.editor-header {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-shrink: 0;
}

.title-input {
  flex: 1;
  :deep(.n-input) {
    border-radius: 8px;
  }
  :deep(.n-input__input-el) {
    font-size: 18px;
    font-weight: 600;
  }
}

.editor-wrap {
  flex: 1;
  min-height: 0;
}

/* 查看模式 */
.wiki-view {
  display: flex;
  flex-direction: column;
  height: 100%;
  min-height: 0;
}

.view-header {
  flex-shrink: 0;
  display: flex;
  align-items: flex-start;
  gap: 16px;
  padding: 22px 32px 18px;
  border-bottom: 1px solid #f1f3f7;
}

.view-header-text {
  flex: 1;
  min-width: 0;
}

.view-header-actions {
  flex-shrink: 0;
  display: flex;
  gap: 8px;
}

.page-title {
  margin: 0;
  font-size: 22px;
  font-weight: 700;
  color: #111827;
  letter-spacing: -.3px;
  word-break: break-word;
}

.page-meta {
  margin-top: 6px;
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 12px;
  color: #9ca3af;
  > svg { color: #9ca3af; }
}

.view-scroll-body {
  flex: 1;
  min-height: 0;
  overflow-y: auto;
  padding: 24px 32px 32px;

  &::-webkit-scrollbar { width: 6px; }
  &::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 3px; }
  &::-webkit-scrollbar-track { background: transparent; }
}

.view-content {
  line-height: 1.85;
  color: #374151;
  font-size: 14px;
  margin-bottom: 32px;

  :deep(h1) { font-size: 1.7em; font-weight: 700; margin: 1.4em 0 .5em; color: #111827; letter-spacing: -.3px; }
  :deep(h2) { font-size: 1.35em; font-weight: 700; margin: 1.2em 0 .4em; color: #1f2937; }
  :deep(h3) { font-size: 1.15em; font-weight: 600; margin: 1em 0 .3em; color: #1f2937; }
  :deep(ul), :deep(ol) { padding-left: 1.5rem; }
  :deep(li) { margin: .25em 0; }
  :deep(blockquote) {
    margin: 1em 0;
    padding: .5em 1rem;
    background: #f9fafb;
    border-left: 3px solid #c7d2fe;
    color: #4b5563;
    border-radius: 0 6px 6px 0;
  }
  :deep(code) {
    background: #f3f4f6;
    color: #be185d;
    border-radius: 4px;
    padding: .15em .45em;
    font-size: .88em;
    font-family: ui-monospace, monospace;
  }
  :deep(pre) {
    background: #0f172a;
    border-radius: 10px;
    padding: 14px 16px;
    overflow-x: auto;
    white-space: pre;

    &::-webkit-scrollbar { height: 6px; }
    &::-webkit-scrollbar-thumb { background: #475569; border-radius: 3px; }
    &::-webkit-scrollbar-track { background: transparent; }

    code {
      background: none;
      color: #e2e8f0;
      padding: 0;
      white-space: pre;
      word-break: normal;
      word-wrap: normal;
      overflow-wrap: normal;
      display: inline-block;
      min-width: 100%;
    }
  }
  :deep(img) { max-width: 100%; border-radius: 8px; margin: .5rem 0; box-shadow: 0 1px 4px rgba(0,0,0,.06); }
  :deep(hr) { border: none; border-top: 1px solid #e5e7eb; margin: 1.5rem 0; }
  :deep(a) { color: #4f46e5; text-decoration: underline; text-underline-offset: 3px; }
}

/* 区段（附件 / 历史） */
.view-section {
  margin-bottom: 20px;
  padding: 14px 16px;
  background: #fafbfc;
  border: 1px solid #eef0f4;
  border-radius: 10px;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 7px;
  font-size: 13px;
  font-weight: 600;
  color: #374151;
  margin-bottom: 12px;

  > svg { color: #6b7280; }
}

.section-count {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 18px;
  height: 18px;
  padding: 0 5px;
  border-radius: 9px;
  font-size: 10px;
  font-weight: 600;
  background: #f1f3f7;
  color: #6b7280;
}

.section-action {
  margin-left: auto;
  display: inline-flex;
  align-items: center;
  gap: 4px;
  height: 24px;
  padding: 0 9px;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  background: #fff;
  font-size: 11px;
  font-weight: 500;
  color: #4b5563;
  cursor: pointer;
  transition: all .12s;
  &:hover { background: #eef2ff; color: #4f46e5; border-color: #c7d2fe; }
}

.section-empty {
  padding: 12px 4px;
  text-align: center;
  color: #9ca3af;
  font-size: 12px;
}

/* 文件列表 */
.file-list {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.file-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 12px;
  border-radius: 8px;
  background: #fff;
  border: 1px solid #eef0f4;
  font-size: 13px;
  transition: border-color .12s;
  &:hover { border-color: #c7d2fe; }
}

.file-icon { color: #6b7280; flex-shrink: 0; }

.file-name {
  flex: 1;
  color: #1f2937;
  font-weight: 500;
  text-decoration: none;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  background: none;
  border: none;
  padding: 0;
  text-align: left;
  cursor: pointer;
  font-size: 13px;
  transition: color .12s;
  &:hover { color: #4f46e5; }
}

.file-size { color: #9ca3af; font-size: 11px; flex-shrink: 0; font-feature-settings: "tnum"; }

.file-action {
  flex-shrink: 0;
  width: 26px; height: 26px;
  border: none;
  border-radius: 6px;
  background: transparent;
  color: #6b7280;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  transition: all .12s;
  &:hover { background: #eef2ff; color: #4f46e5; }

  &--del {
    color: #9ca3af;
    &:hover { background: #fee2e2; color: #dc2626; }
  }
}

/* 历史版本 */
.history-list {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.history-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 12px;
  border-radius: 7px;
  font-size: 12px;
  background: #fff;
  border: 1px solid #eef0f4;
}

.history-version {
  color: #4f46e5;
  font-weight: 600;
  background: #eef2ff;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 11px;
  flex-shrink: 0;
  font-feature-settings: "tnum";
}

.history-editor { flex: 1; color: #374151; font-weight: 500; }

.history-date { color: #9ca3af; font-size: 11px; flex-shrink: 0; font-feature-settings: "tnum"; }

/* 右键菜单 */
.wiki-context-menu {
  position: fixed;
  z-index: 9999;
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  box-shadow: 0 10px 32px rgba(15, 23, 42, .12);
  padding: 4px;
  min-width: 180px;
}

.ctx-item {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  border: none;
  background: none;
  border-radius: 6px;
  font-size: 13px;
  color: #374151;
  cursor: pointer;
  text-align: left;
  transition: all .12s;

  > svg { color: #6b7280; }

  &:hover {
    background: #eef2ff;
    color: #4f46e5;
    > svg { color: #4f46e5; }
  }
}

/* 可见性弹窗 */
.visibility-form {
  display: grid;
  gap: 14px;
}

.visibility-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding: 12px 14px;
  background: #fafbfc;
  border: 1px solid #eef0f4;
  border-radius: 10px;
}

.visibility-label {
  font-size: 13px;
  font-weight: 600;
  color: #1f2937;
}

.visibility-hint {
  font-size: 12px;
  color: #9ca3af;
  margin-top: 2px;
}

.visibility-url {
  padding: 12px 14px;
  background: #eef2ff;
  border: 1px solid #c7d2fe;
  border-radius: 10px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.visibility-code {
  padding: 12px 14px;
  background: #fafbfc;
  border: 1px solid #eef0f4;
  border-radius: 10px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.visibility-url-label {
  font-size: 11px;
  color: #4f46e5;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: .5px;
}

.visibility-url-text {
  font-size: 12px;
  color: #4338ca;
  word-break: break-all;
  font-feature-settings: "tnum";
}
</style>
