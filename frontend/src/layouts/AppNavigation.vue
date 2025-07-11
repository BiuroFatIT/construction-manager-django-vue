<script setup>
import { RouterLink } from 'vue-router'
import { navItems } from './navItems';

const props = defineProps({
  drawer: { type: Boolean, required: true },
  'onUpdate:drawer': { type: Function, required: true },
})

const emit = defineEmits(['update:drawer'])

</script>

<template>
  <v-navigation-drawer
    :model-value="drawer"
    @update:model-value="emit('update:drawer', $event)"
    app
    width="280"
    class="py-2 mt-3"
  >
    <v-list density="compact" nav>
      <template v-for="(item, idx) in navItems" :key="idx">
        <v-list-subheader
          v-if="item.header"
          class="font-weight-bold text-uppercase text-xs tracking-widest opacity-75 my-2"
        >
          {{ item.header }}
        </v-list-subheader>

        <v-list-group v-else-if="item.children" eager>
          <template #activator="{ props: activatorProps }">
            <v-list-item
              v-bind="activatorProps"
              :title="item.title"
              :prepend-icon="item.icon || undefined"
            />
          </template>

          <template v-for="(child, cidx) in item.children" :key="cidx">
            <v-list-group v-if="child.children" eager>
              <template #activator="{ props: childActivatorProps }">
                <v-list-item
                  v-bind="childActivatorProps"
                  :title="child.title"
                  :prepend-icon="child.icon || undefined"
                />
              </template>

              <v-list-item
                v-for="(subchild, scidx) in child.children"
                :key="scidx"
                :to="subchild.to"
                :title="subchild.title"
                :prepend-icon="subchild.icon || undefined"
                :component="RouterLink"
                active-class="bg-primary text-primary-contrast"
              />
            </v-list-group>

            <v-list-item
              v-else
              :to="child.to"
              :title="child.title"
              :prepend-icon="child.icon || undefined"
              :component="RouterLink"
              active-class="bg-primary text-primary-contrast"
            />
          </template>
        </v-list-group>

        <v-list-item
          v-else
          :to="item.to"
          :prepend-icon="item.icon || undefined"
          :title="item.title"
          :component="RouterLink"
          active-class="bg-primary text-primary-contrast"
        />
      </template>
    </v-list>
  </v-navigation-drawer>
</template>
