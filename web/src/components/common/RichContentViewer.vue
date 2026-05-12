<template>
  <div class="rich-viewer" @click.capture="handleClick">
    <editor-content :editor="editor" />
  </div>
</template>

<script setup lang="ts">
import { watch, onBeforeUnmount } from 'vue'
import { useEditor, EditorContent } from '@tiptap/vue-3'
import StarterKit from '@tiptap/starter-kit'
import Image from '@tiptap/extension-image'
import Underline from '@tiptap/extension-underline'
import TextAlign from '@tiptap/extension-text-align'
import Color from '@tiptap/extension-color'
import { TextStyle } from '@tiptap/extension-text-style'
import Highlight from '@tiptap/extension-highlight'
import { api as viewerApi } from 'v-viewer'
import 'viewerjs/dist/viewer.css'

const props = defineProps<{ content?: string | null }>()

const editor = useEditor({
  extensions: [
    StarterKit,
    Underline,
    TextStyle,
    Color,
    Highlight.configure({ multicolor: true }),
    TextAlign.configure({ types: ['heading', 'paragraph'] }),
    Image.configure({ HTMLAttributes: { class: 'editor-img' } }),
  ],
  content: props.content || '',
  editable: false,
  editorProps: {
    attributes: { class: 'prose' },
  },
})

watch(() => props.content, (val) => {
  if (!editor.value) return
  editor.value.commands.setContent(val || '')
})

onBeforeUnmount(() => editor.value?.destroy())

const handleClick = (e: MouseEvent) => {
  const target = e.target as HTMLElement
  if (target.tagName === 'IMG') {
    e.preventDefault()
    viewerApi({ images: [(target as HTMLImageElement).src] })
  }
}
</script>

<style scoped lang="scss">
.rich-viewer {
  :deep(.ProseMirror) {
    outline: none;

    > * + * { margin-top: 0.6em; }

    h1 { font-size: 1.8em; font-weight: 700; }
    h2 { font-size: 1.4em; font-weight: 700; }
    h3 { font-size: 1.2em; font-weight: 600; }
    h4 { font-size: 1.05em; font-weight: 600; }

    p { line-height: 1.75; margin: 0 0 0.4em; }

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
      cursor: zoom-in;
    }
  }
}
</style>
