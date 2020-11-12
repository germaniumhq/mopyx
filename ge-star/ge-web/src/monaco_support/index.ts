
import * as monaco from 'monaco-editor';


const documentReferences: { [name: string]: number } = {}

export function createModel(
    code: string,
    language: string,
    uri: string): monaco.editor.ITextModel {

    const documentUri = monaco.Uri.parse(uri)
    const existingModel = monaco.editor.getModel(documentUri)

    if (existingModel) {
        return existingModel as monaco.editor.ITextModel
    }

    return monaco.editor.createModel(code, language, documentUri)
}

export function createEditor(
    container: any,
    code: string,
    language: string,
    uri: string): monaco.editor.IStandaloneCodeEditor {

    documentReferences[uri] = (documentReferences[uri] || 0) + 1;

    const editor = monaco.editor.create(container, {
        model: createModel(code, language, uri),
        language: language,
        automaticLayout: true,
        lineNumbersMinChars: 2,
        glyphMargin: true,
        lightbulb: {
            enabled: true
        },
    });

    return editor;
}

export function unregisterEditor(
    uri: string
): void {
    documentReferences[uri] = (documentReferences[uri] || 0) - 1;
    
    if (documentReferences[uri] != 0) {
        return
    }

    const documentUri = monaco.Uri.parse(uri)
    const existingModel = monaco.editor.getModel(documentUri)

    existingModel?.dispose()
}
