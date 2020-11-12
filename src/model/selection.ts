
/* eslint no-console: ["off", { allow: ["warn", "error"] }] */

import { Vue, Component, Model } from 'vue-property-decorator'


/**
 * An item that can be selected from the UI. It can be a
 * file, a tab, a test, etc. We assume selectable elements
 * can be dragged and dropped around the application.
 */
export interface Selectable {
    uri: string
}

/**
 * A selection of 0, 1 or more selectables. The active selection
 * is only one at a time
 */
export interface Selection {
    label: string

    // selection operations
    select(selectable: Selectable): void
    add(selectable: Selectable): void
    delete(selectable: Selectable): void
    clear(): void

    contains(selectable: Selectable): boolean
}

@Component({})
class ActiveSelection extends Vue implements Selection {
    private items: { [name: string] :  Selectable} = {}
    private selectedItems: Map<String, Selectable> = new Map<String, Selectable>()

    get label() {
        this.items // we create a dependency on the selectedItems, since
                   // Vue can't monitor sets

        if (this.selectedItems.size == 0) {
            return "<<empty>>"
        }

        let result = ""

        this.selectedItems.forEach((it) => {
            result += `${it.uri}, `
        })

        return result
    }

    select(selectable: Selectable): void {
        this.items = {}
        this.items[selectable.uri] = selectable

        this.selectedItems.clear()
        this.selectedItems.set(selectable.uri, selectable)

        this.$emit("selection-change", this.items)
    }

    add(selectable: Selectable): void {
        this.items[selectable.uri] = selectable
        this.items = { ... this.items }

        this.selectedItems.set(selectable.uri, selectable)

        this.$emit("selection-change", this.items)
    }

    delete(selectable: Selectable): void {
        delete this.items[selectable.uri]
        this.items = { ... this.items }

        this.selectedItems.delete(selectable.uri)

        this.$emit("selection-change", this.items)
    }

    clear(): void {
        this.items = {}

        this.selectedItems.clear()

        this.$emit("selection-change", this.items)
    }

    contains(selectable: Selectable): boolean {
        return !! this.items[selectable.uri]
    }
}


export const selection = new ActiveSelection()
