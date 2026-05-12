<template>
  <Teleport to="body">
    <Transition name="fp-fade">
      <div
        v-if="show && url && type !== 'image'"
        class="fp-overlay"
        @click.self="close"
      >
        <div class="fp-header">
          <span class="fp-title-text">{{ title }}</span>
          <button class="fp-close-btn" @click="close">
            <Icon icon="fluent:dismiss-20-regular" :width="22" :height="22" />
          </button>
        </div>

        <div :key="url" class="fp-body">
          <!-- Video -->
          <div v-if="type === 'video'" class="fp-video-wrap">
            <div v-if="videoLoading" class="fp-video-loading">
              <n-spin size="large" />
              <span>视频加载中...</span>
            </div>
            <div v-if="videoError" class="fp-download">
              <Icon icon="fluent:video-off-20-regular" :width="56" :height="56" class="fp-dl-icon" />
              <p class="fp-dl-name">视频无法嵌入播放</p>
              <n-button type="primary" tag="a" :href="url" target="_blank" rel="noopener">
                <template #icon><Icon icon="fluent:open-20-regular" /></template>
                在新窗口打开
              </n-button>
            </div>
            <video
              v-show="!videoLoading && !videoError"
              :src="url"
              controls
              preload="metadata"
              class="fp-video"
              @loadedmetadata="videoLoading = false"
              @error="videoError = true; videoLoading = false"
            />
          </div>

          <!-- Office / Download -->
          <div v-else class="fp-office-shell">
            <VueOfficeDocx v-if="type === 'docx'" :src="url" class="fp-office" />
            <VueOfficeExcel v-else-if="type === 'excel'" :src="url" class="fp-office" />
            <VueOfficePptx v-else-if="type === 'pptx'" :src="url" class="fp-office" />
            <VueOfficePdf v-else-if="type === 'pdf'" :src="url" class="fp-office" />

            <div v-else class="fp-download">
              <Icon :icon="fileIcon" :width="60" :height="60" class="fp-dl-icon" />
              <p class="fp-dl-name">{{ title }}</p>
              <n-button type="primary" tag="a" :href="url" target="_blank" rel="noopener">
                <template #icon>
                  <Icon icon="fluent:arrow-download-20-regular" />
                </template>
                下载文件
              </n-button>
            </div>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
import { computed, ref, watch, onUnmounted } from 'vue'
import { NButton, NSpin } from 'naive-ui'
import { Icon } from '@iconify/vue'
import { api as viewerApi } from 'v-viewer'
import 'viewerjs/dist/viewer.css'
import VueOfficeDocx from '@vue-office/docx'
import VueOfficeExcel from '@vue-office/excel'
import VueOfficePptx from '@vue-office/pptx'
import VueOfficePdf from '@vue-office/pdf'
import '@vue-office/docx/lib/index.css'
import '@vue-office/excel/lib/index.css'

export interface PreviewFile {
  url?: string | null
  fileName?: string | null
  fileObjectName?: string | null
}

const props = defineProps<{ show: boolean; file: PreviewFile | null }>()
const emit = defineEmits<{ 'update:show': [boolean] }>()

const close = () => emit('update:show', false)

const url = computed(() => props.file?.url ?? '')

const title = computed(() => {
  const name = props.file?.fileName || props.file?.fileObjectName || ''
  if (name) return name
  try {
    return new URL(url.value).pathname.split('/').pop() || '文件预览'
  } catch {
    return '文件预览'
  }
})

const ext = computed(() => {
  const name = title.value
  const dot = name.lastIndexOf('.')
  return dot >= 0 ? name.slice(dot + 1).toLowerCase() : ''
})

const type = computed(() => {
  const e = ext.value
  if (['jpg', 'jpeg', 'png', 'gif', 'webp', 'svg', 'bmp'].includes(e)) return 'image'
  if (['mp4', 'webm', 'ogg', 'mov', 'avi'].includes(e)) return 'video'
  if (['docx', 'doc'].includes(e)) return 'docx'
  if (['xlsx', 'xls'].includes(e)) return 'excel'
  if (['pptx', 'ppt'].includes(e)) return 'pptx'
  if (e === 'pdf') return 'pdf'
  return 'download'
})

const fileIcon = computed(() => {
  const t = type.value
  if (t === 'video') return 'fluent:video-20-regular'
  if (t === 'docx') return 'fluent:document-text-20-regular'
  if (t === 'excel') return 'fluent:table-20-regular'
  if (t === 'pptx') return 'fluent:presenter-20-regular'
  if (t === 'pdf') return 'fluent:document-pdf-20-regular'
  return 'fluent:document-20-regular'
})

// 图片类型：交给 v-viewer，不显示自定义遮罩
watch(() => props.show, (val) => {
  if (val && url.value && type.value === 'image') {
    viewerApi({ images: [url.value] })
    emit('update:show', false)
  }
})

// 视频加载状态：每次打开时重置
const videoLoading = ref(false)
const videoError = ref(false)

watch([() => props.show, () => props.file], () => {
  if (props.show && type.value === 'video') {
    videoLoading.value = true
    videoError.value = false
  }
})

// ESC 关闭
const onKeydown = (e: KeyboardEvent) => {
  if (e.key === 'Escape' && props.show && type.value !== 'image') close()
}
document.addEventListener('keydown', onKeydown)
onUnmounted(() => document.removeEventListener('keydown', onKeydown))
</script>

<style scoped lang="scss">
.fp-overlay {
  position: fixed;
  inset: 0;
  z-index: 9000;
  background: rgba(0, 0, 0, 0.88);
  display: flex;
  flex-direction: column;
}

.fp-header {
  flex-shrink: 0;
  height: 54px;
  padding: 0 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.fp-title-text {
  flex: 1;
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  color: rgba(255, 255, 255, 0.9);
  font-size: 14px;
}

.fp-close-btn {
  flex-shrink: 0;
  width: 36px;
  height: 36px;
  border: none;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.1);
  color: rgba(255, 255, 255, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background 0.15s;

  &:hover {
    background: rgba(255, 255, 255, 0.2);
    color: #fff;
  }
}

.fp-body {
  flex: 1;
  min-height: 0;
  padding: 0 20px 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.fp-video-wrap {
  width: 100%;
  height: calc(100vh - 54px - 20px);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 16px;
}

.fp-video-loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  color: rgba(255, 255, 255, 0.7);
  font-size: 14px;
}

.fp-video {
  width: 100%;
  max-height: 100%;
  border-radius: 8px;
  outline: none;
  background: #000;
}

.fp-office-shell {
  width: 100%;
  height: calc(100vh - 54px - 20px);
  background: #fff;
  border-radius: 8px;
  overflow: auto;

  // 覆盖 @vue-office/pptx 写死的 540px 内联高度
  :deep(.pptx-preview-wrapper) {
    height: calc(100vh - 54px - 20px) !important;
    overflow-y: auto !important;
  }
}

.fp-office {
  width: 100%;
}

.fp-download {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  color: rgba(255, 255, 255, 0.6);
}

.fp-dl-icon {
  color: rgba(255, 255, 255, 0.4);
}

.fp-dl-name {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.85);
  max-width: 400px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.fp-fade-enter-active,
.fp-fade-leave-active {
  transition: opacity 0.2s ease;
}

.fp-fade-enter-from,
.fp-fade-leave-to {
  opacity: 0;
}
</style>
