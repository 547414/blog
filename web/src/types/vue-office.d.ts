declare module '@vue-office/docx' {
  import { DefineComponent } from 'vue'
  const component: DefineComponent<{ src: string; requestOptions?: Record<string, unknown> }>
  export default component
}

declare module '@vue-office/excel' {
  import { DefineComponent } from 'vue'
  const component: DefineComponent<{ src: string; requestOptions?: Record<string, unknown> }>
  export default component
}

declare module '@vue-office/pptx' {
  import { DefineComponent } from 'vue'
  const component: DefineComponent<{ src: string }>
  export default component
}

declare module '@vue-office/pdf' {
  import { DefineComponent } from 'vue'
  const component: DefineComponent<{ src: string }>
  export default component
}
