<template>
  <div class="rich-editor">
    <!-- 工具栏 -->
    <div class="editor-toolbar">
      <div class="toolbar-group">
        <n-button-group size="small">
          <n-button :type="editor?.isActive('bold') ? 'primary' : 'default'" @click="editor?.chain().focus().toggleBold().run()">
            <Icon icon="fluent:text-bold-20-regular"/>
          </n-button>
          <n-button :type="editor?.isActive('italic') ? 'primary' : 'default'" @click="editor?.chain().focus().toggleItalic().run()">
            <Icon icon="fluent:text-italic-20-regular"/>
          </n-button>
          <n-button :type="editor?.isActive('underline') ? 'primary' : 'default'" @click="editor?.chain().focus().toggleUnderline().run()">
            <Icon icon="fluent:text-underline-20-regular"/>
          </n-button>
          <n-button :type="editor?.isActive('strike') ? 'primary' : 'default'" @click="editor?.chain().focus().toggleStrike().run()">
            <Icon icon="fluent:text-strikethrough-20-regular"/>
          </n-button>
        </n-button-group>
      </div>

      <div class="toolbar-divider"/>

      <div class="toolbar-group">
        <n-button-group size="small">
          <n-button v-for="level in [1,2,3,4]" :key="level"
                    :type="editor?.isActive('heading', { level }) ? 'primary' : 'default'"
                    @click="editor?.chain().focus().toggleHeading({ level } as any).run()">
            H{{ level }}
          </n-button>
        </n-button-group>
      </div>

      <div class="toolbar-divider"/>

      <div class="toolbar-group">
        <n-button-group size="small">
          <n-button :type="editor?.isActive('bulletList') ? 'primary' : 'default'" @click="editor?.chain().focus().toggleBulletList().run()">
            <Icon icon="fluent:text-bullet-list-20-regular"/>
          </n-button>
          <n-button :type="editor?.isActive('orderedList') ? 'primary' : 'default'" @click="editor?.chain().focus().toggleOrderedList().run()">
            <Icon icon="fluent:text-number-list-ltr-20-regular"/>
          </n-button>
          <n-button :type="editor?.isActive('blockquote') ? 'primary' : 'default'" @click="editor?.chain().focus().toggleBlockquote().run()">
            <Icon icon="fluent:text-quote-20-regular"/>
          </n-button>
          <n-button :type="editor?.isActive('code') ? 'primary' : 'default'" @click="editor?.chain().focus().toggleCode().run()">
            <Icon icon="fluent:code-20-regular"/>
          </n-button>
        </n-button-group>
      </div>

      <div class="toolbar-divider"/>

      <div class="toolbar-group">
        <n-button-group size="small">
          <n-button :type="editor?.isActive({ textAlign: 'left' }) ? 'primary' : 'default'" @click="editor?.chain().focus().setTextAlign('left').run()">
            <Icon icon="fluent:text-align-left-20-regular"/>
          </n-button>
          <n-button :type="editor?.isActive({ textAlign: 'center' }) ? 'primary' : 'default'" @click="editor?.chain().focus().setTextAlign('center').run()">
            <Icon icon="fluent:text-align-center-20-regular"/>
          </n-button>
          <n-button :type="editor?.isActive({ textAlign: 'right' }) ? 'primary' : 'default'" @click="editor?.chain().focus().setTextAlign('right').run()">
            <Icon icon="fluent:text-align-right-20-regular"/>
          </n-button>
        </n-button-group>
      </div>

      <div class="toolbar-divider"/>

      <div class="toolbar-group">
        <n-popover trigger="click">
          <template #trigger>
            <n-button size="small"><Icon icon="fluent:color-20-regular"/></n-button>
          </template>
          <div class="color-panel">
            <div class="color-grid">
              <div v-for="c in textColors" :key="c" class="color-dot" :style="{background: c}" @click="editor?.chain().focus().setColor(c).run()"/>
            </div>
            <n-button size="tiny" text @click="editor?.chain().focus().unsetColor().run()">清除颜色</n-button>
          </div>
        </n-popover>
        <n-popover trigger="click">
          <template #trigger>
            <n-button size="small"><Icon icon="fluent:paint-bucket-20-regular"/></n-button>
          </template>
          <div class="color-panel">
            <div class="color-grid">
              <div v-for="c in bgColors" :key="c" class="color-dot" :style="{background: c}" @click="editor?.chain().focus().setHighlight({color: c}).run()"/>
            </div>
            <n-button size="tiny" text @click="editor?.chain().focus().unsetHighlight().run()">清除背景</n-button>
          </div>
        </n-popover>
      </div>

      <div class="toolbar-divider"/>

      <div class="toolbar-group">
        <n-button size="small" @click="handleImageUpload">
          <Icon icon="fluent:image-20-regular"/>
        </n-button>
        <n-button size="small" @click="editor?.chain().focus().setHorizontalRule().run()">
          <Icon icon="fluent:line-horizontal-1-20-regular"/>
        </n-button>
      </div>

      <div class="toolbar-divider"/>

      <div class="toolbar-group">
        <n-button-group size="small">
          <n-button :disabled="!editor?.can().undo()" @click="editor?.chain().focus().undo().run()">
            <Icon icon="fluent:arrow-undo-20-regular"/>
          </n-button>
          <n-button :disabled="!editor?.can().redo()" @click="editor?.chain().focus().redo().run()">
            <Icon icon="fluent:arrow-redo-20-regular"/>
          </n-button>
        </n-button-group>
      </div>
    </div>

    <!-- 编辑区 -->
    <div class="editor-body">
      <editor-content :editor="editor" class="editor-content"/>
    </div>

    <input type="file" ref="fileInputRef" accept="image/*" style="display:none" @change="handleFileChange"/>
  </div>
</template>

<script setup lang="ts">
import {ref, watch, onBeforeUnmount} from 'vue'
import {Icon} from '@iconify/vue'
import {NButton, NButtonGroup, NPopover, useNotification} from 'naive-ui'
import {useEditor, EditorContent} from '@tiptap/vue-3'
import StarterKit from '@tiptap/starter-kit'
import Image from '@tiptap/extension-image'
import Underline from '@tiptap/extension-underline'
import TextAlign from '@tiptap/extension-text-align'
import Color from '@tiptap/extension-color'
import {TextStyle} from '@tiptap/extension-text-style'
import Highlight from '@tiptap/extension-highlight'
import {apiUploadFile} from '@/api/storageApi.ts'

interface Props {
  modelValue: string | null
}

const props = defineProps<Props>()
const emit = defineEmits<{
  'update:modelValue': [value: string]
}>()

const notification = useNotification()
const fileInputRef = ref<HTMLInputElement>()

const textColors = ['#000','#374151','#ef4444','#f97316','#eab308','#22c55e','#3b82f6','#8b5cf6','#ec4899','#fff']
const bgColors = ['#fef9c3','#fce7f3','#ede9fe','#dbeafe','#dcfce7','#ffedd5','#fee2e2','#f3f4f6','#fff','transparent']

const editor = useEditor({
  extensions: [
    StarterKit,
    Underline,
    TextStyle,
    Color,
    Highlight.configure({multicolor: true}),
    TextAlign.configure({types: ['heading', 'paragraph']}),
    Image.configure({HTMLAttributes: {class: 'editor-img'}}),
  ],
  content: props.modelValue || '',
  editorProps: {
    attributes: {class: 'prose focus:outline-none'},
  },
  onUpdate: ({editor}) => {
    emit('update:modelValue', editor.getHTML())
  }
})

watch(() => props.modelValue, (val) => {
  if (!editor.value) return
  if (val !== editor.value.getHTML()) {
    editor.value.commands.setContent(val || '')
  }
})

onBeforeUnmount(() => editor.value?.destroy())

const handleImageUpload = () => fileInputRef.value?.click()

const handleFileChange = (e: Event) => {
  const file = (e.target as HTMLInputElement).files?.[0]
  if (!file) return
  if (file.size > 10 * 1024 * 1024) {
    notification.error({title: '图片不能超过 10MB', duration: 2000})
    return
  }
  apiUploadFile({file, fileName: file.name, fileSize: file.size}).then(res => {
    if (res.code === 200 && res.data) {
      editor.value?.chain().focus().setImage({src: res.data.url || ''}).run()
    } else {
      notification.error({title: '上传失败', content: res.message, duration: 2000})
    }
  })
  ;(e.target as HTMLInputElement).value = ''
}
</script>

<style scoped lang="scss">
.rich-editor {
  display: flex;
  flex-direction: column;
  height: 100%;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  overflow: hidden;
}

.editor-toolbar {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 6px;
  padding: 8px 12px;
  background: #f9fafb;
  border-bottom: 1px solid #e5e7eb;
  flex-shrink: 0;
}

.toolbar-group {
  display: flex;
  align-items: center;
  gap: 4px;
}

.toolbar-divider {
  width: 1px;
  height: 20px;
  background: #e5e7eb;
  flex-shrink: 0;
}

.editor-body {
  flex: 1;
  overflow-y: auto;
  padding: 20px 24px;
  background: #fff;

  &::-webkit-scrollbar {
    width: 6px;
  }
  &::-webkit-scrollbar-thumb {
    background: #d1d5db;
    border-radius: 3px;
  }
}

.editor-content {
  height: 100%;

  :deep(.ProseMirror) {
    outline: none;
    min-height: 300px;

    > * + * { margin-top: 0.6em; }

    h1 { font-size: 1.8em; font-weight: 700; }
    h2 { font-size: 1.4em; font-weight: 700; }
    h3 { font-size: 1.2em; font-weight: 600; }
    h4 { font-size: 1.05em; font-weight: 600; }

    p { line-height: 1.75; }

    ul, ol {
      padding-left: 1.5rem;
      li { margin: 0.2rem 0; }
    }

    blockquote {
      border-left: 3px solid #d1d5db;
      padding-left: 1rem;
      color: #6b7280;
      margin: 1rem 0;
    }

    code {
      background: #f3f4f6;
      border-radius: 3px;
      padding: 0.1em 0.4em;
      font-size: 0.875em;
      color: #374151;
    }

    pre {
      background: #0f172a;
      border-radius: 8px;
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

    hr { border: none; border-top: 1px solid #e5e7eb; margin: 1.5rem 0; }

    img.editor-img {
      max-width: 100%;
      border-radius: 6px;
      margin: 0.5rem 0;
    }
  }
}

.color-panel {
  padding: 8px;
  min-width: 160px;
}

.color-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 6px;
  margin-bottom: 8px;
}

.color-dot {
  width: 24px;
  height: 24px;
  border-radius: 4px;
  border: 1px solid #e5e7eb;
  cursor: pointer;
  transition: transform 0.15s;
  &:hover { transform: scale(1.15); }
}
</style>
