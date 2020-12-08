import {GeStarEditor, TreeNode} from "./ui"
import {selection} from './selection'

import router from '@/router'

enum Section {
    OVERVIEW,
    DATA,
}

const germaniumTreeNode: TreeNode = {
    label: "root",
    uri: "file:/",
    children: [
        {
            uri: "file:/a",
            label: "a"
        },
        {
            uri: "file:/b",
            label: "b",
            children: [
                {
                    uri: "file:/b/x",
                    label: "x"
                }
            ]
        },
        {
            uri: "file:/c",
            label: "c",
            icon: 'fa-file'
        }
    ]
}

const open_editors: Array<GeStarEditor> = [
    {
        key: "editor1",
        activeDocument: "a",
        documents: []
    },
]


class UiModel {
    left_navigation = true
    backdrop = false

    get section() {
        if (router.currentRoute.path.startsWith("/data")) {
            return "data"
        } else if (router.currentRoute.path.startsWith("/reports")) {
            return "reports"
        } else if (router.currentRoute.path.startsWith("/projects")) {
            return "projects"
        }

        return "overview"
    }
}


class Model {
    ui = new UiModel
    projects = {
        ge: {
            files: germaniumTreeNode
        }
    }
    open_editors = open_editors
    selection = selection
}

const model = new Model()

export default model
