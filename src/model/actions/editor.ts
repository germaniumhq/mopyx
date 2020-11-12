import { CodeEditor } from '../ui';

export function registerDocument(
    editor: CodeEditor,
    path: string,
    language: string,
    content: string
) {
    if (!editor.documents.length) {
        editor.activeDocument = path
    }

    editor.documents.push({
        key: path,
        label: getFileName(path),
        icon: "file",
        language: language,
        content: content
    })
}

export function unregisterDocument(
    editor: CodeEditor,
    path: string,
) {
    let i;

    for (i = 0; i < editor.documents.length; i++) {
        const document = editor.documents[i]

        if (document.key != path) {
            continue
        }

        editor.documents.splice(i, 1)
        break;
    }

    if (i < editor.documents.length) {
        editor.activeDocument = editor.documents[i].key
    } else if (i > 0) {
        editor.activeDocument = editor.documents[i - 1].key
    } else {
        editor.activeDocument = "";
    }
}

function getFileName(path: string) : string {
    const pathTokens = path.split("/")
    return pathTokens[pathTokens.length - 1]
}
