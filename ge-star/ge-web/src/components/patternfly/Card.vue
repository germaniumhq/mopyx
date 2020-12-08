<template>
  <div class="pf-c-card" id="card-action-example-2">
    <div class="pf-c-card__header">
      <div class="pf-c-card__actions">
        <div class="pf-c-dropdown">
          <button class="pf-c-dropdown__toggle pf-m-plain" type="button" id="card-action-example-2-dropdown-kebab-right-aligned-button" aria-expanded="false" aria-label="Actions">
            <i class="fas fa-ellipsis-v" aria-hidden="true"></i>
          </button>
          <ul class="pf-c-dropdown__menu" aria-labelledby="card-action-example-2-dropdown-kebab-right-aligned-button" hidden>
            <li>
              <a class="pf-c-dropdown__menu-item" href="#">Link</a>
            </li>
            <li>
              <button class="pf-c-dropdown__menu-item" type="button">Action</button>
            </li>
            <li>
              <a class="pf-c-dropdown__menu-item pf-m-disabled" href="#" aria-disabled="true" tabindex="-1">Disabled link</a>
            </li>
            <li>
              <button class="pf-c-dropdown__menu-item" type="button" disabled>Disabled action</button>
            </li>
            <li class="pf-c-divider" role="separator"></li>
            <li>
              <a class="pf-c-dropdown__menu-item" href="#">Separated link</a>
            </li>
          </ul>
        </div>
        <input type="checkbox" id="card-action-example-2-check" name="card-action-example-2-check" aria-labelledby="card-action-example-2-check-label" />
      </div>
      <div class="pf-c-card__title" id="card-action-example-2-check-label">This is a really really really really really really really really really really long title</div>
    </div>
    <div class="pf-c-card__body">Body</div>
    <div class="pf-c-card__footer">Footer</div>
  </div>
</template>

<script lang="ts">
import { Prop, Vue, Component } from 'vue-property-decorator'

@Component({})
export default class Card extends Vue {
}
</script>
