<template>
  <div class="wp-layout">
    <!-- 顶部栏 -->
    <header class="wp-header">
      <div class="wp-header-left">
        <button v-if="!isProjectIndex" class="wp-menu-btn" @click="sidebarOpen = !sidebarOpen">
          <Icon :icon="sidebarOpen ? 'fluent:dismiss-20-regular' : 'fluent:list-20-regular'" :width="18"/>
        </button>
        <button class="wp-brand" @click="router.push('/')">
          <span class="wp-header-icon">
            <Icon icon="fluent:book-20-filled" :width="16"/>
          </span>
          <span class="wp-header-title">{{ isProjectIndex ? '公开项目' : (currentProject?.name || 'Wiki') }}</span>
        </button>
        <span v-if="page" class="wp-header-sep">/</span>
        <span v-if="page" class="wp-header-page-title">{{ page.title }}</span>
      </div>
      <div class="wp-search">
        <Icon icon="fluent:search-20-regular" :width="14" class="wp-search-icon"/>
        <input
            v-model="searchKeyword"
            class="wp-search-input"
            placeholder="搜索公开 Wiki"
            autocomplete="off"
            autocapitalize="off"
            autocorrect="off"
            spellcheck="false"
            @input="handleSearchInput"
            @focus="searchFocused = true"
            @blur="handleSearchBlur"
            @keyup.enter="handleEnterSearch"
        />
        <div
            v-if="searchFocused && (searchLoading || searchResultList.length || searchKeyword)"
            class="wp-search-popover"
            @scroll="handleSearchScroll"
        >
          <div v-if="searchLoading && searchResultList.length === 0" class="wp-search-empty">
            <n-spin size="small"/>
          </div>
          <button
              v-for="item in searchResultList"
              :key="item.pageId"
              class="wp-search-item"
              @mousedown.prevent="handleSelectSearchItem(item)"
          >
            <div class="wp-search-item-title">
              <span>{{ item.pageTitle }}</span>
              <Icon v-if="item.requireAuth" icon="fluent:lock-closed-16-regular" :width="12"/>
            </div>
            <div class="wp-search-item-project">{{ item.projectName }} · {{ item.projectCode }}</div>
          </button>
          <div v-if="!searchLoading && searchKeyword && searchResultList.length === 0" class="wp-search-empty">
            无匹配结果
          </div>
          <div v-if="searchLoading && searchResultList.length > 0" class="wp-search-more">
            <n-spin size="small"/>
          </div>
        </div>
      </div>
    </header>

    <main v-if="isProjectIndex" class="wp-project-main">
      <section class="wp-project-hero">
        <div>
          <h1>公开项目</h1>
          <p>浏览已公开 Wiki 的项目</p>
        </div>
        <div class="wp-project-search">
          <Icon icon="fluent:search-20-regular" :width="16"/>
          <input
              v-model="projectSearch"
              placeholder="搜索项目或公开 Wiki"
              autocomplete="off"
              @input="handleProjectSearchInput"
          />
        </div>
      </section>

      <section v-if="projectLoading" class="wp-project-state">
        <n-spin size="large"/>
      </section>
      <section v-else-if="!projectList.length" class="wp-project-state">
        <div class="wp-empty-icon">
          <Icon icon="fluent:folder-open-20-regular" :width="34"/>
        </div>
        <p class="wp-empty-title">暂无公开项目</p>
        <p class="wp-empty-desc">有公开 Wiki 节点的项目会显示在这里</p>
      </section>
      <section v-else class="wp-project-grid">
        <button
            v-for="project in projectList"
            :key="project.id"
            class="wp-project-card"
            @click="handleOpenProject(project.id)"
        >
          <div class="wp-project-card-head">
            <div class="wp-project-avatar">
              <Icon icon="fluent:folder-20-filled" :width="18"/>
            </div>
            <Icon icon="fluent:chevron-right-20-regular" :width="18" class="wp-project-arrow"/>
          </div>
          <h2>{{ project.name }}</h2>
          <p class="wp-project-desc">{{ project.desc || project.code }}</p>
          <div class="wp-project-meta">
            <span>{{ project.wikiCount }} 篇 Wiki</span>
            <span v-if="project.latestUpdatedAt">更新于 {{ formatDate(project.latestUpdatedAt) }}</span>
          </div>
        </button>
      </section>

      <footer v-if="projectTotalPage > 1" class="wp-project-pager">
        <button :disabled="projectPageIndex <= 1 || projectLoading" @click="changeProjectPage(projectPageIndex - 1)">
          <Icon icon="fluent:chevron-left-20-regular" :width="14"/>上一页
        </button>
        <span>{{ projectPageIndex }} / {{ projectTotalPage }}</span>
        <button :disabled="projectPageIndex >= projectTotalPage || projectLoading" @click="changeProjectPage(projectPageIndex + 1)">
          下一页<Icon icon="fluent:chevron-right-20-regular" :width="14"/>
        </button>
      </footer>
    </main>

    <div v-else class="wp-body">
      <!-- 遮罩（移动端） -->
      <div v-if="sidebarOpen" class="wp-overlay" @click="sidebarOpen = false" />

      <!-- 左侧树 -->
      <aside class="wp-sidebar" :class="{ 'wp-sidebar--open': sidebarOpen }">
        <div v-if="treeLoading" class="wp-sidebar-empty">
          <n-spin size="small" />
        </div>
        <div v-else-if="!tree.length" class="wp-sidebar-empty">
          <span>暂无公开页面</span>
        </div>
        <div v-else class="wp-tree">
          <PublicTreeNode
              v-for="node in tree"
              :key="node.id"
              :node="node"
              :active-id="currentPageId"
              @select="handleSelectPage"
          />
        </div>
      </aside>

      <!-- 右侧内容 -->
      <main class="wp-main">
        <div v-if="treeLoading" class="wp-empty">
          <n-spin size="large" />
        </div>

        <div v-else-if="!currentPageId" class="wp-empty">
          <div class="wp-empty-icon">
            <Icon icon="fluent:book-open-20-regular" :width="36"/>
          </div>
          <p class="wp-empty-title">浏览公开知识库</p>
          <p class="wp-empty-desc">从左侧目录选择一个页面查看内容</p>
          <button class="wp-toc-btn" @click="sidebarOpen = true">
            <Icon icon="fluent:list-20-regular" :width="14"/>查看目录
          </button>
        </div>

        <div v-else-if="pageLoading" class="wp-empty">
          <n-spin size="large" />
        </div>

        <div v-else-if="needLogin" class="wp-empty">
          <div class="wp-empty-icon wp-empty-icon--lock">
            <Icon icon="fluent:lock-closed-20-regular" :width="36"/>
          </div>
          <p class="wp-empty-title">需要授权码</p>
          <p class="wp-empty-desc">请输入授权码查看此页面</p>
          <div class="wp-auth-code">
            <n-input
                v-model:value="authCode"
                placeholder="授权码"
                autocomplete="off"
                autocapitalize="off"
                autocorrect="off"
                spellcheck="false"
                @keyup.enter="handleSubmitAuthCode"
            />
            <n-button type="primary" class="wp-auth-submit" @click="handleSubmitAuthCode">
              查看
            </n-button>
          </div>
        </div>

        <div v-else-if="pageError" class="wp-empty">
          <div class="wp-empty-icon wp-empty-icon--err">
            <Icon icon="fluent:document-dismiss-20-regular" :width="36"/>
          </div>
          <p class="wp-empty-title">无法访问</p>
          <p class="wp-empty-desc">{{ pageError }}</p>
        </div>

        <div v-else-if="page" class="wp-content-wrap">
          <header class="wp-content-header">
            <h1 class="wp-content-title">{{ page.title }}</h1>
            <div class="wp-content-meta">
              <Icon icon="fluent:clock-20-regular" :width="13"/>
              <span>更新于 {{ formatDate(page.updatedAt) }}</span>
            </div>
          </header>
          <div class="wp-content-body">
            <RichContentViewer :content="page.content" />
          </div>

          <!-- 附件 -->
          <section v-if="fileList.length" class="wp-attach-section">
            <div class="wp-attach-title">
              <Icon icon="fluent:attach-20-regular" :width="14"/>
              <span>附件</span>
              <span class="wp-attach-count">{{ fileList.length }}</span>
            </div>
            <div class="wp-attach-list">
              <div
                  v-for="f in fileList"
                  :key="f.id"
                  class="wp-attach-item"
                  @click="handlePreviewFile(f)"
              >
                <Icon icon="fluent:document-20-regular" :width="16" class="wp-attach-icon"/>
                <span class="wp-attach-name">{{ f.fileName }}</span>
                <span class="wp-attach-size">{{ formatFileSize(f.fileSize) }}</span>
                <button class="wp-attach-action" title="下载" @click.stop="handleDownloadFile(f)">
                  <Icon icon="fluent:arrow-download-20-regular" :width="13"/>
                </button>
                <button class="wp-attach-action wp-attach-action--preview" title="预览" @click.stop="handlePreviewFile(f)">
                  <Icon icon="fluent:open-20-regular" :width="13"/>
                </button>
              </div>
            </div>
          </section>
        </div>
      </main>
    </div>

    <FilePreviewModal v-model:show="previewVisible" :file="previewFile" />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, defineComponent, h } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Icon } from '@iconify/vue'
import { NButton, NInput, NSpin } from 'naive-ui'
import dayjs from 'dayjs'
import RichContentViewer from '@/components/common/RichContentViewer.vue'
import FilePreviewModal, { type PreviewFile } from '@/components/common/FilePreviewModal.vue'
import { downloadFromUrl } from '@/utils/file.ts'
import {
  apiGetPublicWikiPageTree,
  apiGetPublicWikiPageDetail,
  apiGetPublicWikiPageFileList,
  apiSearchPublicWiki,
  type PublicWikiSearchParams,
  type WikiPageTreeItem,
  type WikiPageDetail,
  type WikiPageFileDetail,
  type PublicWikiSearchItem,
} from '@/api/wikiApi.ts'
import {
  apiGetPublicWikiProjectPage,
  apiGetPublicWikiProjectDetail,
  type WikiProjectPageParams,
  type WikiProjectDetail,
  type PublicWikiProjectDetail,
} from '@/api/wikiProjectApi.ts'

const PublicTreeNode = defineComponent({
  name: 'PublicTreeNode',
  props: {
    node: { type: Object as () => WikiPageTreeItem, required: true },
    activeId: { type: String, default: null },
    depth: { type: Number, default: 0 },
  },
  emits: ['select'],
  setup(props, { emit }) {
    const expanded = ref(true)
    return () => {
      const { node, activeId, depth } = props
      const isActive = node.id === activeId
      const lockIcon = node.requireAuth
          ? h(Icon, { icon: 'fluent:lock-closed-16-regular', width: 11, class: 'text-gray-400 flex-shrink-0' })
          : null
      return h('div', { class: 'pt-node' }, [
        h('div', {
          class: ['pt-node-row', isActive && 'active'],
          style: { paddingLeft: `${10 + depth * 14}px` },
          onClick: () => emit('select', node.id),
        }, [
          node.childList?.length
              ? h('span', {
                class: 'pt-expand',
                onClick: (e: Event) => { e.stopPropagation(); expanded.value = !expanded.value },
              }, h(Icon, { icon: expanded.value ? 'fluent:chevron-down-16-regular' : 'fluent:chevron-right-16-regular', width: 11 }))
              : h('span', { class: 'pt-expand-placeholder' }),
          h(Icon, { icon: 'fluent:document-20-regular', width: 13, class: 'text-gray-400 flex-shrink-0' }),
          h('span', { class: 'pt-node-title' }, node.title),
          lockIcon,
        ]),
        expanded.value && node.childList?.length
            ? h('div', node.childList.map(child =>
                h(PublicTreeNode, {
                  node: child, activeId, depth: depth + 1,
                  onSelect: (id: string) => emit('select', id),
                })
            ))
            : null,
      ])
    }
  },
})

const route = useRoute()
const router = useRouter()

const currentPageId = computed(() => route.query.page as string | undefined)
const urlAccessCode = computed(() => route.query.accessCode as string | undefined)
const projectId = computed(() => route.params.projectId as string | undefined)
const isProjectIndex = computed(() => !projectId.value)
const publicPath = computed(() => projectId.value ? `/public-wiki/${projectId.value}` : '/')

const sidebarOpen = ref(false)
const treeLoading = ref(false)
const pageLoading = ref(false)
const needLogin = ref(false)
const pageError = ref('')
const authCode = ref('')
const tree = ref<WikiPageTreeItem[]>([])
const page = ref<WikiPageDetail | null>(null)
const currentProject = ref<WikiProjectDetail | null>(null)
const fileList = ref<WikiPageFileDetail[]>([])
const previewVisible = ref(false)
const previewFile = ref<PreviewFile | null>(null)
const searchKeyword = ref('')
const searchFocused = ref(false)
const searchLoading = ref(false)
const searchResultList = ref<PublicWikiSearchItem[]>([])
const searchPage = ref(1)
const searchHasMore = ref(false)
const searchPageSize = 20
let searchTimer: number | null = null
let searchRequestSeq = 0
const projectSearch = ref('')
const projectLoading = ref(false)
const projectList = ref<PublicWikiProjectDetail[]>([])
const projectPageIndex = ref(1)
const projectPageSize = 12
const projectTotalCount = ref(0)
let projectSearchTimer: number | null = null

const projectTotalPage = computed(() => {
  return Math.max(1, Math.ceil(projectTotalCount.value / projectPageSize))
})

const formatDate = (d: string | null) => d ? dayjs(d).format('YYYY-MM-DD HH:mm') : ''

const formatFileSize = (size: number | null) => {
  if (!size) return '-'
  if (size < 1024) return `${size}B`
  if (size < 1024 * 1024) return `${(size / 1024).toFixed(1)}KB`
  return `${(size / 1024 / 1024).toFixed(1)}MB`
}

const handlePreviewFile = (f: WikiPageFileDetail) => {
  previewFile.value = { url: f.url, fileName: f.fileName }
  previewVisible.value = true
}

const handleDownloadFile = (f: WikiPageFileDetail) => {
  downloadFromUrl(f.url, f.fileName)
}

const getStoredAuthCode = (pageId: string) => {
  return sessionStorage.getItem(`wikiAuthCode:${pageId}`) || ''
}

const loadFiles = (pageId: string, inputAuthCode: string | null = null) => {
  const code = inputAuthCode ?? getStoredAuthCode(pageId)
  apiGetPublicWikiPageFileList(pageId, code, projectId.value).then(res => {
    if (res.code === 200) fileList.value = res.data || []
    else fileList.value = []
  }).catch(() => { fileList.value = [] })
}

const loadTree = () => {
  if (isProjectIndex.value) return
  treeLoading.value = true
  apiGetPublicWikiPageTree(projectId.value).then(res => {
    if (res.code === 200) tree.value = res.data || []
  }).finally(() => { treeLoading.value = false })
}

const loadProjectDetail = () => {
  if (!projectId.value) {
    currentProject.value = null
    return
  }
  apiGetPublicWikiProjectDetail(projectId.value).then(res => {
    currentProject.value = res.code === 200 ? res.data : null
  }).catch(() => {
    currentProject.value = null
  })
}

const loadProjectPage = () => {
  projectLoading.value = true
  const pageParams: WikiProjectPageParams = {
    pageIndex: projectPageIndex.value,
    pageSize: projectPageSize,
    search: projectSearch.value.trim() || null,
  }
  apiGetPublicWikiProjectPage(pageParams).then(res => {
    if (res.code === 200) {
      projectList.value = res.data?.data || []
      projectTotalCount.value = res.data?.filterCount || 0
    } else {
      projectList.value = []
      projectTotalCount.value = 0
    }
  }).catch(() => {
    projectList.value = []
    projectTotalCount.value = 0
  }).finally(() => {
    projectLoading.value = false
  })
}

const loadPage = (pageId: string, inputAuthCode: string | null = null) => {
  pageLoading.value = true
  needLogin.value = false
  pageError.value = ''
  page.value = null
  fileList.value = []
  const code = inputAuthCode ?? getStoredAuthCode(pageId)
  apiGetPublicWikiPageDetail(pageId, code, projectId.value).then(res => {
    if (res.code === 200) {
      page.value = res.data
      if (code) sessionStorage.setItem(`wikiAuthCode:${pageId}`, code)
      loadFiles(pageId, code)
    } else if (res.message?.includes('授权码')) {
      needLogin.value = true
      pageError.value = res.message || ''
    } else {
      pageError.value = res.message || '页面不存在或未公开'
    }
  }).catch(() => {
    pageError.value = '页面不存在或未公开'
  }).finally(() => { pageLoading.value = false })
}

const handleSubmitAuthCode = () => {
  if (!currentPageId.value) return
  loadPage(currentPageId.value, authCode.value)
}

const handleSelectPage = (pageId: string) => {
  router.push({path: publicPath.value, query: {page: pageId}})
  sidebarOpen.value = false
}

const handleOpenProject = (targetProjectId: string) => {
  router.push({path: `/public-wiki/${targetProjectId}`})
}

const handleProjectSearchInput = () => {
  if (projectSearchTimer !== null) window.clearTimeout(projectSearchTimer)
  projectSearchTimer = window.setTimeout(() => {
    projectPageIndex.value = 1
    loadProjectPage()
  }, 250)
}

const changeProjectPage = (pageIndex: number) => {
  projectPageIndex.value = Math.min(Math.max(1, pageIndex), projectTotalPage.value)
  loadProjectPage()
}

const doSearch = (append = false) => {
  const keyword = searchKeyword.value.trim()
  if (!keyword) {
    searchResultList.value = []
    searchLoading.value = false
    searchPage.value = 1
    searchHasMore.value = false
    return
  }
  if (append && (searchLoading.value || !searchHasMore.value)) return
  const nextPage = append ? searchPage.value + 1 : 1
  const requestSeq = ++searchRequestSeq
  searchLoading.value = true
  const searchParams: PublicWikiSearchParams = {
    search: keyword,
    page: nextPage,
    pageSize: searchPageSize,
  }
  apiSearchPublicWiki(searchParams).then(res => {
    if (requestSeq !== searchRequestSeq || keyword !== searchKeyword.value.trim()) return
    const nextList = res.code === 200 ? (res.data?.dataList || []) : []
    searchResultList.value = append ? [...searchResultList.value, ...nextList] : nextList
    searchHasMore.value = res.code === 200 ? !!res.data?.hasMore : false
    searchPage.value = nextPage
  }).catch(() => {
    if (requestSeq !== searchRequestSeq) return
    if (!append) searchResultList.value = []
    searchHasMore.value = false
  }).finally(() => {
    if (requestSeq === searchRequestSeq) searchLoading.value = false
  })
}

const handleSearchInput = () => {
  searchFocused.value = true
  if (searchTimer !== null) window.clearTimeout(searchTimer)
  if (!searchKeyword.value.trim()) {
    searchRequestSeq += 1
    searchResultList.value = []
    searchHasMore.value = false
    searchLoading.value = false
    return
  }
  searchTimer = window.setTimeout(() => doSearch(false), 250)
}

const handleSearchScroll = (event: Event) => {
  const target = event.target as HTMLElement
  const reachBottom = target.scrollTop + target.clientHeight >= target.scrollHeight - 24
  if (reachBottom) doSearch(true)
}

const handleSearchBlur = () => {
  window.setTimeout(() => {
    searchFocused.value = false
  }, 120)
}

const handleEnterSearch = () => {
  const first = searchResultList.value[0]
  if (first) handleSelectSearchItem(first)
}

const handleSelectSearchItem = (item: PublicWikiSearchItem) => {
  const targetPath = `/public-wiki/${item.projectId}`
  router.push({path: targetPath, query: {page: item.pageId}})
  searchFocused.value = false
  searchKeyword.value = ''
  searchResultList.value = []
  searchHasMore.value = false
}

watch([() => currentPageId.value, () => urlAccessCode.value, () => projectId.value], ([id, code]) => {
  if (isProjectIndex.value) {
    page.value = null
    needLogin.value = false
    pageError.value = ''
    fileList.value = []
    return
  }
  authCode.value = id ? (code || getStoredAuthCode(id)) : ''
  if (id) loadPage(id, code || null)
  else { page.value = null; needLogin.value = false; pageError.value = ''; fileList.value = [] }
}, { immediate: true })

watch(() => projectId.value, () => {
  if (isProjectIndex.value) {
    tree.value = []
    sidebarOpen.value = false
    currentProject.value = null
    loadProjectPage()
  } else {
    loadProjectDetail()
    loadTree()
  }
}, { immediate: true })
</script>

<style scoped lang="scss">
/* ══ 方案 A · 编辑级 Shopify 风 ══════════════════════════
   暖白 #FBFAF7 + 草绿 #1B7F4D，文字优先、留白多
   ───────────────────────────────────────────────────── */
$bg:            #FBFAF7;
$panel:         #F6F4EE;
$ink:           #1B1D1A;
$mute:          #6B6F67;
$line:          rgba(27, 29, 26, 0.10);
$accent:        #1B7F4D;
$accent-dark:   #166640; // accent 加深 ~6%
$accent-darker: #155534; // accent 加深 ~10%
$accent-soft:   rgba(27, 127, 77, 0.10);
$accent-hover:  rgba(27, 127, 77, 0.06);
$radius:        10px;

.wp-layout {
  display: flex;
  flex-direction: column;
  height: 100vh;
  overflow: hidden;
  background: $bg;
  color: $ink;
  font-family: 'Inter', 'Noto Sans SC', system-ui, -apple-system, sans-serif;
  letter-spacing: -0.005em;
}

/* ── 顶部栏 ────────────────────────────────────────── */
.wp-header {
  flex-shrink: 0;
  height: 56px;
  padding: 0 24px;
  border-bottom: 1px solid $line;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  background: $bg;
}

.wp-header-left {
  display: flex;
  align-items: center;
  gap: 10px;
  min-width: 0;
  flex: 1;
}

.wp-brand {
  min-width: 0;
  border: none;
  background: transparent;
  padding: 0;
  display: inline-flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  flex-shrink: 0;
}

.wp-header-icon {
  flex-shrink: 0;
  width: 26px; height: 26px;
  border-radius: 6px;
  background: $accent;
  color: #fff;
  display: flex; align-items: center; justify-content: center;
  letter-spacing: -0.02em;
}

.wp-header-title {
  font-size: 14.5px;
  font-weight: 600;
  color: $ink;
  letter-spacing: -0.01em;
  flex-shrink: 0;
}

.wp-header-sep {
  color: $line;
  flex-shrink: 0;
  font-size: 14px;
}

.wp-header-page-title {
  font-size: 13px;
  color: $mute;
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.wp-menu-btn {
  width: 32px;
  height: 32px;
  border: 1px solid $line;
  border-radius: 6px;
  background: $bg;
  color: $mute;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  flex-shrink: 0;
  transition: all .12s;
  &:hover { background: $accent-hover; color: $accent; border-color: $accent-soft; }
}

.wp-login-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  height: 32px;
  padding: 0 14px;
  border: 1px solid $line;
  border-radius: 6px;
  background: $bg;
  font-size: 12.5px;
  font-weight: 500;
  color: $ink;
  cursor: pointer;
  text-decoration: none;
  flex-shrink: 0;
  transition: all .12s;

  &:hover { background: $accent; color: #fff; border-color: $accent; }
}

.wp-search {
  position: relative;
  width: min(360px, 34vw);
  flex-shrink: 0;
}

.wp-search-icon {
  position: absolute;
  left: 12px;
  top: 50%;
  z-index: 1;
  color: $mute;
  pointer-events: none;
  transform: translateY(-50%);
}

.wp-search-input {
  width: 100%;
  height: 34px;
  padding: 0 12px 0 34px;
  border: 1px solid $line;
  border-radius: 8px;
  outline: none;
  background: #fff;
  color: $ink;
  font-size: 13px;
  transition: all .12s;

  &::placeholder { color: rgba(107, 111, 103, .72); }
  &:focus {
    border-color: rgba(27, 127, 77, .35);
    box-shadow: 0 0 0 3px $accent-soft;
  }
}

.wp-search-popover {
  position: absolute;
  top: 40px;
  right: 0;
  z-index: 60;
  width: min(420px, calc(100vw - 32px));
  max-height: 360px;
  overflow-y: auto;
  padding: 6px;
  border: 1px solid $line;
  border-radius: 10px;
  background: #fff;
  box-shadow: 0 18px 48px rgba(27, 29, 26, .14);

  &::-webkit-scrollbar { width: 4px; }
  &::-webkit-scrollbar-thumb { background: $line; border-radius: 2px; }
  &::-webkit-scrollbar-track { background: transparent; }
}

.wp-search-item {
  width: 100%;
  padding: 10px 11px;
  border: 0;
  border-radius: 8px;
  background: transparent;
  color: $ink;
  text-align: left;
  cursor: pointer;

  &:hover { background: $accent-hover; }
}

.wp-search-item-title {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  font-size: 13px;
  font-weight: 600;
}

.wp-search-item-title span {
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.wp-search-item-project {
  margin-top: 3px;
  overflow: hidden;
  color: $mute;
  font-size: 12px;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.wp-search-empty {
  padding: 16px 12px;
  color: $mute;
  font-size: 12px;
  text-align: center;
}

.wp-search-more {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 8px 0 6px;
}

.wp-auth-code {
  width: min(360px, 100%);
  display: flex;
  align-items: center;
  gap: 8px;
}

.wp-auth-submit {
  flex-shrink: 0;
}

/* ── 主体布局 ──────────────────────────────────────── */
.wp-body {
  flex: 1;
  min-height: 0;
  display: flex;
  overflow: hidden;
  position: relative;
}

.wp-project-main {
  flex: 1;
  min-height: 0;
  overflow-y: auto;
  padding: 48px 56px 72px;

  &::-webkit-scrollbar { width: 6px; }
  &::-webkit-scrollbar-thumb { background: $line; border-radius: 3px; }
  &::-webkit-scrollbar-track { background: transparent; }
}

.wp-project-hero {
  max-width: 1120px;
  margin: 0 auto 24px;
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 24px;

  h1 {
    margin: 0;
    color: $ink;
    font-size: 34px;
    font-weight: 720;
    line-height: 1.16;
    letter-spacing: -0.02em;
  }

  p {
    margin: 8px 0 0;
    color: $mute;
    font-size: 14px;
  }
}

.wp-project-search {
  width: min(420px, 42vw);
  height: 40px;
  padding: 0 13px;
  display: flex;
  align-items: center;
  gap: 9px;
  border: 1px solid $line;
  border-radius: 8px;
  background: #fff;
  color: $mute;
  flex-shrink: 0;
  transition: all .12s;

  &:focus-within {
    border-color: rgba(27, 127, 77, .35);
    box-shadow: 0 0 0 3px $accent-soft;
  }

  input {
    flex: 1;
    min-width: 0;
    border: 0;
    outline: none;
    background: transparent;
    color: $ink;
    font-size: 13px;
  }

  input::placeholder { color: rgba(107, 111, 103, .72); }
}

.wp-project-grid {
  max-width: 1120px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 14px;
}

.wp-project-card {
  min-height: 188px;
  padding: 18px;
  border: 1px solid $line;
  border-radius: 8px;
  background: #fff;
  color: $ink;
  text-align: left;
  cursor: pointer;
  transition: border-color .12s, transform .12s, box-shadow .12s;

  &:hover {
    border-color: rgba(27, 127, 77, .22);
    box-shadow: 0 16px 38px rgba(27, 29, 26, .08);
    transform: translateY(-1px);

    .wp-project-arrow { color: $accent; transform: translateX(2px); }
  }

  h2 {
    margin: 16px 0 8px;
    color: $ink;
    font-size: 18px;
    font-weight: 700;
    line-height: 1.3;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
}

.wp-project-card-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.wp-project-avatar {
  width: 34px;
  height: 34px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 7px;
  background: $accent-soft;
  color: $accent;
}

.wp-project-arrow {
  color: $mute;
  transition: all .12s;
}

.wp-project-desc {
  min-height: 40px;
  margin: 0;
  color: $mute;
  font-size: 13px;
  line-height: 1.55;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.wp-project-meta {
  margin-top: 18px;
  padding-top: 12px;
  border-top: 1px solid $line;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  color: $mute;
  font-size: 12px;

  span {
    min-width: 0;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
}

.wp-project-state {
  max-width: 1120px;
  min-height: 360px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
}

.wp-project-pager {
  max-width: 1120px;
  margin: 24px auto 0;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 14px;
  color: $mute;
  font-size: 13px;

  button {
    height: 34px;
    padding: 0 13px;
    border: 1px solid $line;
    border-radius: 7px;
    background: #fff;
    color: $ink;
    display: inline-flex;
    align-items: center;
    gap: 5px;
    cursor: pointer;
    transition: all .12s;

    &:hover:not(:disabled) {
      border-color: $accent;
      background: $accent;
      color: #fff;
    }

    &:disabled {
      opacity: .45;
      cursor: not-allowed;
    }
  }
}

/* 移动端遮罩 */
.wp-overlay {
  display: none;
  position: fixed;
  inset: 56px 0 0 0;
  background: rgba(20, 22, 18, .35);
  z-index: 99;
}

/* ── 侧边栏 ────────────────────────────────────────── */
.wp-sidebar {
  width: 280px;
  flex-shrink: 0;
  border-right: 1px solid $line;
  overflow-y: auto;
  padding: 18px 10px 24px;
  background: $panel;

  &::-webkit-scrollbar { width: 4px; }
  &::-webkit-scrollbar-thumb { background: $line; border-radius: 2px; }
  &::-webkit-scrollbar-track { background: transparent; }
}

.wp-sidebar-empty {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
  color: $mute;
  font-size: 12.5px;
}

/* ── 主内容 ────────────────────────────────────────── */
.wp-main {
  flex: 1;
  min-width: 0;
  overflow-y: auto;
  background: $bg;

  &::-webkit-scrollbar { width: 6px; }
  &::-webkit-scrollbar-thumb { background: $line; border-radius: 3px; }
  &::-webkit-scrollbar-track { background: transparent; }
}

.wp-empty {
  min-height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 32px;
  text-align: center;
}

.wp-empty-icon {
  width: 72px; height: 72px;
  border-radius: 50%;
  background: $accent-soft;
  color: $accent;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 18px;

  &--lock { background: rgba(180, 83, 9, 0.10); color: #B45309; }
  &--err  { background: rgba(185, 28, 28, 0.10); color: #b91c1c; }
}

.wp-empty-title {
  margin: 0;
  font-size: 18px;
  font-weight: 700;
  color: $ink;
  letter-spacing: -0.02em;
}

.wp-empty-desc {
  margin: 6px 0 18px;
  font-size: 13.5px;
  color: $mute;
}

.wp-toc-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  height: 34px;
  padding: 0 16px;
  border: 1px solid $line;
  border-radius: 6px;
  background: $bg;
  font-size: 13px;
  font-weight: 500;
  color: $ink;
  cursor: pointer;
  transition: all .12s;
  &:hover { background: $accent; color: #fff; border-color: $accent; }
}

.wp-content-wrap {
  max-width: 880px;
  margin: 0 auto;
  padding: 56px 56px 96px;
}

.wp-content-header {
  margin-bottom: 36px;
  padding-bottom: 24px;
  border-bottom: 1px solid $line;
}

.wp-content-title {
  font-size: 36px;
  font-weight: 700;
  color: $ink;
  margin: 0 0 12px;
  line-height: 1.18;
  letter-spacing: -0.025em;
}

.wp-content-meta {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 12.5px;
  color: $mute;

  > svg { color: $mute; }
}

.wp-content-body {
  max-width: 720px;

  :deep(.ProseMirror) {
    font-size: 15px;
    line-height: 1.78;
    color: $ink;
  }

  :deep(p) { margin: 0.9em 0; }
  :deep(h1) { font-size: 1.7em; font-weight: 700; margin: 1.5em 0 .5em; color: $ink; letter-spacing: -0.02em; }
  :deep(h2) { font-size: 1.35em; font-weight: 700; margin: 1.3em 0 .45em; color: $ink; letter-spacing: -0.015em; }
  :deep(h3) { font-size: 1.15em; font-weight: 600; margin: 1.1em 0 .35em; color: $ink; }
  :deep(ul), :deep(ol) { padding-left: 1.5rem; }
  :deep(li) { margin: .3em 0; }
  :deep(blockquote) {
    margin: 1em 0;
    padding: .5em 1rem;
    background: $panel;
    border-left: 3px solid $accent;
    color: $mute;
    border-radius: 0 6px 6px 0;
  }
  :deep(code) {
    background: $panel;
    color: $accent;
    border-radius: 4px;
    padding: .15em .45em;
    font-size: .88em;
    font-family: 'JetBrains Mono', ui-monospace, monospace;
  }
  :deep(pre) {
    background: #1B1D1A;
    border-radius: $radius;
    padding: 16px 18px;
    overflow-x: auto;
    white-space: pre;

    &::-webkit-scrollbar { height: 6px; }
    &::-webkit-scrollbar-thumb { background: #3f413e; border-radius: 3px; }
    &::-webkit-scrollbar-track { background: transparent; }

    code {
      background: none;
      color: #F6F4EE;
      padding: 0;
      white-space: pre;
      word-break: normal;
      word-wrap: normal;
      overflow-wrap: normal;
      display: inline-block;
      min-width: 100%;
    }
  }
  :deep(img) { max-width: 100%; border-radius: $radius * 0.8; margin: .8rem 0; }
  :deep(a) {
    color: $accent;
    text-decoration: underline;
    text-underline-offset: 3px;
    text-decoration-thickness: 1px;
    &:hover { text-decoration-thickness: 2px; }
  }
  :deep(hr) { border: none; border-top: 1px solid $line; margin: 1.8rem 0; }
}

/* ── 附件区 ────────────────────────────────────────── */
.wp-attach-section {
  max-width: 720px;
  margin-top: 40px;
  padding: 18px 20px;
  background: $panel;
  border: 1px solid $line;
  border-radius: $radius;
}

.wp-attach-title {
  display: flex;
  align-items: center;
  gap: 7px;
  font-size: 13px;
  font-weight: 600;
  color: $ink;
  margin-bottom: 12px;

  > svg { color: $mute; }
}

.wp-attach-count {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 18px;
  height: 18px;
  padding: 0 5px;
  border-radius: 9px;
  font-size: 10px;
  font-weight: 600;
  background: $accent-soft;
  color: $accent;
}

.wp-attach-list {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.wp-attach-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 8px 8px 14px;
  border: 1px solid $line;
  border-radius: $radius * 0.8;
  background: $bg;
  font-size: 13px;
  cursor: pointer;
  text-align: left;
  transition: all .12s;

  &:hover {
    border-color: $accent-soft;
    background: $accent-hover;

    .wp-attach-icon { color: $accent; }
    .wp-attach-name { color: $accent; }
  }
}

.wp-attach-action {
  flex-shrink: 0;
  width: 28px; height: 28px;
  border: none;
  border-radius: 6px;
  background: transparent;
  color: $mute;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  transition: all .12s;
  &:hover { background: $accent-soft; color: $accent; }
}

.wp-attach-icon { color: $mute; flex-shrink: 0; transition: color .12s; }

.wp-attach-name {
  flex: 1;
  min-width: 0;
  color: $ink;
  font-weight: 500;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  transition: color .12s;
}

.wp-attach-size {
  color: $mute;
  font-size: 11px;
  flex-shrink: 0;
  font-feature-settings: "tnum";
}


/* ── 树节点 ────────────────────────────────────────── */
:deep(.pt-node-row) {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 10px;
  cursor: pointer;
  border-radius: 6px;
  margin: 1px 0;
  font-size: 13.5px;
  font-weight: 500;
  color: $ink;
  line-height: 1.4;
  transition: background .12s, color .12s;

  &:hover { background: $accent-hover; }
  &.active {
    background: $accent-soft;
    color: $accent;
    font-weight: 600;
  }
}

:deep(.pt-expand) {
  width: 14px;
  height: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  color: $mute;
  opacity: 0.8;
  border-radius: 3px;
  &:hover { color: $accent; opacity: 1; }
}

:deep(.pt-expand-placeholder) { width: 14px; flex-shrink: 0; }

:deep(.pt-node-title) {
  flex: 1;
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* ── Naive UI 主色覆盖（input/button） ─────────────── */
:deep(.n-input) {
  --n-border-radius: 6px;
  --n-border: 1px solid #{$line};
  --n-border-hover: 1px solid #{$accent-soft};
  --n-border-focus: 1px solid #{$accent};
  --n-box-shadow-focus: 0 0 0 2px #{$accent-soft};
  --n-caret-color: #{$accent};
  --n-color: #{$bg};
}

:deep(.wp-auth-submit.n-button) {
  --n-color: #{$accent};
  --n-color-hover: #{$accent-dark};
  --n-color-pressed: #{$accent-darker};
  --n-color-focus: #{$accent};
  --n-border: 1px solid #{$accent};
  --n-border-hover: 1px solid #{$accent-dark};
  --n-border-pressed: 1px solid #{$accent-darker};
  --n-border-focus: 1px solid #{$accent};
  --n-border-radius: 6px;
  --n-text-color: #fff;
  --n-text-color-hover: #fff;
  --n-text-color-pressed: #fff;
  --n-text-color-focus: #fff;
}

/* ── 移动端 ────────────────────────────────────────── */
@media (max-width: 768px) {
  .wp-overlay { display: block; }

  .wp-sidebar {
    position: fixed;
    top: 56px;
    left: 0;
    bottom: 0;
    z-index: 100;
    transform: translateX(-100%);
    transition: transform .25s ease;
    width: 82%;
    max-width: 320px;

    &.wp-sidebar--open {
      transform: translateX(0);
      box-shadow: 8px 0 30px rgba(0, 0, 0, .18);
    }
  }

  .wp-content-wrap {
    padding: 28px 20px 80px;
  }

  .wp-content-title { font-size: 26px; }

  .wp-content-body {
    :deep(.ProseMirror) { font-size: 15px; line-height: 1.78; }
    :deep(img.editor-img) { width: 100%; }
    :deep(pre) { overflow-x: auto; }
    :deep(table) { display: block; overflow-x: auto; }
  }

  .wp-attach-section { margin-top: 28px; }

  .wp-header-page-title,
  .wp-header-sep { display: none; }

  .wp-header { padding: 0 16px; }

  .wp-search {
    width: min(52vw, 240px);
  }

  .wp-search-popover {
    right: -4px;
  }

  .wp-project-main {
    padding: 28px 18px 54px;
  }

  .wp-project-hero {
    display: block;
    margin-bottom: 18px;

    h1 { font-size: 28px; }
  }

  .wp-project-search {
    width: 100%;
    margin-top: 18px;
  }

  .wp-project-grid {
    grid-template-columns: 1fr;
    gap: 12px;
  }

  .wp-project-card {
    min-height: 166px;
    padding: 16px;
  }

  .wp-project-meta {
    display: block;

    span {
      display: block;
      margin-top: 4px;
    }
  }

  .wp-project-pager {
    justify-content: space-between;
  }
}

@media (min-width: 769px) and (max-width: 1080px) {
  .wp-project-main {
    padding: 42px 32px 64px;
  }

  .wp-project-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}
</style>
