<template>
    <div :class="containerCssClasses">
        <div ref="editorContainer"
             class="ge-code-editor"
             :style="style"></div>
    </div>
</template>

<style scoped>
.ge-code-editor-container {
    position: absolute;
    left: 0;
    right: 0;
    top: 0;
    bottom: 0;
}

.hidden {
    visibility: hidden;
}
</style>

<script lang="ts">
import { Component, Vue, Prop, Watch } from 'vue-property-decorator';
import { CodeDocument } from '@/model/ui'

import * as monaco from 'monaco-editor';
import { editor } from 'monaco-editor/esm/vs/editor/editor.api';

import { getLanguageService, TextDocument } from "vscode-json-languageservice";
import { createEditor, createModel } from '@/monaco_support'


monaco.languages.registerCompletionItemProvider('python', {
    provideCompletionItems(model, position, context, token): monaco.Thenable<monaco.languages.CompletionList> {
        const document = createDocument(model);
        const wordUntil = model.getWordUntilPosition(position);
        const defaultRange = new monaco.Range(position.lineNumber, wordUntil.startColumn, position.lineNumber, wordUntil.endColumn);

        return Promise.resolve({
            suggestions: [
                {
                    label: "wut",
                    kind: 0,
                    insertText: "wut",
                    range: defaultRange
                }
            ]
        })
        // const jsonDocument = jsonService.parseJSONDocument(document);
        // return jsonService.doComplete(document, m2p.asPosition(position.lineNumber, position.column), jsonDocument).then((list) => {
        //     return p2m.asCompletionResult(list, defaultRange);
        // });
    },

    resolveCompletionItem(model, position, item, token): monaco.languages.CompletionItem | monaco.Thenable<monaco.languages.CompletionItem> {
        return item
        // return jsonService.doResolve(m2p.asCompletionItem(item)).then(result => p2m.asCompletionItem(result, item.range));
    }
});


function createDocument(model: monaco.editor.IReadOnlyModel) {
    return TextDocument.create("inmemory://test.py", model.getModeId(), model.getVersionId(), model.getValue());
}


@Component({})
export default class MonacoCodeEditor extends Vue {
    private editor: editor.IStandaloneCodeEditor | null = null;

    @Prop() document!: CodeDocument

    @Prop() hidden!: boolean

    public mounted() {
        this.editor = createEditor(
            this.$refs.editorContainer as any,
            this.document.content,
            this.document.language,
            this.document.key)

        // const decorations = this.editor.deltaDecorations([], [
        //     {
        //         range: new monaco.Range(3, 1, 3, 1),
        //         options: {
        //             isWholeLine: true,
        //             className: 'ge-code-breakpoint-code',
        //             glyphMarginClassName: 'ge-code-breakpoint-decorator',
        //         },
        //     },
        // ]);
    }

    public get style(): {[name: string]: string} {
        return {
            width: '100%',
            bottom: '0',
            top: '0',
            position: 'absolute',
        };
    }

    public setValue(text: string): void {
        if (!this.editor) {
            return;
        }

        this.editor.setValue(text);
    }

    get containerCssClasses() {
        const result: { [name: string] : boolean } = {}

        result['ge-code-editor-container'] = true

        if (this.hidden) {
            result['hidden'] = true
        }

        return result
    }
}
</script>

<style lang="scss">
.ge-code-editor-container {
    position: relative;
}

.ge-code-editor {
    position: absolute;
    bottom: 0;
    top: 0;
    left: 0;
    bottom: 0;
}

.ge-code-breakpoint-decorator {
    background: #cc3333;
    border-radius: 50%;

    &:before {
      content: "";
      color: white;
      font-family: "Font Awesome 5 Free";
      font-size: 0.7em;
      text-shadow: -1px -1px 2px #770000;
      position: relative;
      top: -1px;
      left: 5px;
    }
}
.ge-code-breakpoint-code {
	background: lightblue;
}
</style>
