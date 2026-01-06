<script setup lang="ts">
import { ref, onMounted } from "vue";
import { getMenuList, createMenu, updateMenu, deleteMenu } from "@/api/system";
import { message } from "@/utils/message";
import { ElMessageBox } from "element-plus";

defineOptions({
  name: "MenuManagement"
});

const loading = ref(true);
const dataList = ref([]);
const dialogVisible = ref(false);
const dialogTitle = ref("Add Menu");
const formRef = ref();

const form = ref({
  id: undefined,
  title: "",
  path: "",
  component: "",
  icon: "",
  sort: 0,
  parent_id: null
});

const rules = {
  title: [{ required: true, message: "Title is required", trigger: "blur" }],
  path: [{ required: true, message: "Path is required", trigger: "blur" }]
};

const fetchData = async () => {
  loading.value = true;
  try {
    const res = await getMenuList();
    dataList.value = res.data;
  } finally {
    loading.value = false;
  }
};

const handleAdd = (parentId = null) => {
  dialogTitle.value = "Add Menu";
  form.value = {
    id: undefined,
    title: "",
    path: "",
    component: "",
    icon: "",
    sort: 0,
    parent_id: parentId
  };
  dialogVisible.value = true;
};

const handleEdit = (row) => {
  dialogTitle.value = "Edit Menu";
  form.value = {
    id: row.id,
    title: row.title,
    path: row.path,
    component: row.component,
    icon: row.icon,
    sort: row.sort,
    parent_id: row.parent_id
  };
  dialogVisible.value = true;
};

const handleDelete = (row) => {
  ElMessageBox.confirm(`Are you sure to delete menu ${row.title}?`, "Warning", {
    type: "warning"
  }).then(async () => {
    await deleteMenu(row.id);
    message("Menu deleted", { type: "success" });
    fetchData();
  });
};

const handleSubmit = async () => {
  await formRef.value.validate(async (valid) => {
    if (valid) {
      if (form.value.id) {
        await updateMenu(form.value.id, form.value);
        message("Menu updated", { type: "success" });
      } else {
        await createMenu(form.value);
        message("Menu created", { type: "success" });
      }
      dialogVisible.value = false;
      fetchData();
    }
  });
};

onMounted(() => {
  fetchData();
});
</script>

<template>
  <div class="main">
    <el-card>
      <template #header>
        <div class="flex justify-between">
          <span>Menu Management</span>
          <el-button type="primary" @click="handleAdd(null)">Add Root Menu</el-button>
        </div>
      </template>
      
      <el-table
        :data="dataList"
        v-loading="loading"
        style="width: 100%"
        row-key="id"
        default-expand-all
        :tree-props="{ children: 'children', hasChildren: 'hasChildren' }"
      >
        <el-table-column prop="title" label="Title" />
        <el-table-column prop="path" label="Path" />
        <el-table-column prop="component" label="Component" />
        <el-table-column prop="icon" label="Icon" />
        <el-table-column prop="sort" label="Sort" />
        <el-table-column label="Actions" width="250">
          <template #default="{ row }">
            <el-button link type="primary" @click="handleEdit(row)">Edit</el-button>
            <el-button link type="primary" @click="handleAdd(row.id)">Add Submenu</el-button>
            <el-button link type="danger" @click="handleDelete(row)">Delete</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog v-model="dialogVisible" :title="dialogTitle">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="100px">
        <el-form-item label="Parent ID" prop="parent_id">
            <el-input v-model="form.parent_id" disabled placeholder="Root" />
        </el-form-item>
        <el-form-item label="Title" prop="title">
          <el-input v-model="form.title" />
        </el-form-item>
        <el-form-item label="Path" prop="path">
          <el-input v-model="form.path" />
        </el-form-item>
        <el-form-item label="Component" prop="component">
          <el-input v-model="form.component" placeholder="e.g. system/user/index" />
        </el-form-item>
        <el-form-item label="Icon" prop="icon">
          <el-input v-model="form.icon" />
        </el-form-item>
        <el-form-item label="Sort" prop="sort">
          <el-input-number v-model="form.sort" :min="0" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">Cancel</el-button>
        <el-button type="primary" @click="handleSubmit">Confirm</el-button>
      </template>
    </el-dialog>
  </div>
</template>
