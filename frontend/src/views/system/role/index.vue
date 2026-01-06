<script setup lang="ts">
import { ref, onMounted } from "vue";
import { getRoleList, createRole, updateRole, deleteRole, getMenuList } from "@/api/system";
import { message } from "@/utils/message";
import { ElMessageBox, ElTree } from "element-plus";

defineOptions({
  name: "RoleManagement"
});

const loading = ref(true);
const dataList = ref([]);
const menuList = ref([]);
const dialogVisible = ref(false);
const dialogTitle = ref("Add Role");
const formRef = ref();
const treeRef = ref<InstanceType<typeof ElTree>>();

const form = ref({
  id: undefined,
  name: "",
  code: "",
  description: "",
  menu_ids: []
});

const rules = {
  name: [{ required: true, message: "Name is required", trigger: "blur" }],
  code: [{ required: true, message: "Code is required", trigger: "blur" }]
};

const fetchData = async () => {
  loading.value = true;
  try {
    const res = await getRoleList();
    dataList.value = res.data;
  } finally {
    loading.value = false;
  }
};

const fetchMenus = async () => {
    const res = await getMenuList();
    menuList.value = res.data;
};

const handleAdd = () => {
  dialogTitle.value = "Add Role";
  form.value = {
    id: undefined,
    name: "",
    code: "",
    description: "",
    menu_ids: []
  };
  dialogVisible.value = true;
  if(treeRef.value) treeRef.value.setCheckedKeys([]);
};

const handleEdit = (row) => {
  dialogTitle.value = "Edit Role";
  form.value = {
    id: row.id,
    name: row.name,
    code: row.code,
    description: row.description,
    menu_ids: row.menu_ids
  };
  dialogVisible.value = true;
  // Wait for dialog to open and tree to render
  setTimeout(() => {
      if(treeRef.value) treeRef.value.setCheckedKeys(row.menu_ids);
  }, 0);
};

const handleDelete = (row) => {
  ElMessageBox.confirm(`Are you sure to delete role ${row.name}?`, "Warning", {
    type: "warning"
  }).then(async () => {
    await deleteRole(row.id);
    message("Role deleted", { type: "success" });
    fetchData();
  });
};

const handleSubmit = async () => {
  await formRef.value.validate(async (valid) => {
    if (valid) {
      // Get checked keys (including half-checked if needed, but backend usually expects full selection logic)
      // For now, let's just take checked keys
      const checkedKeys = treeRef.value!.getCheckedKeys();
      // If we want parent nodes to be included even if partially checked, use getHalfCheckedKeys()
      // But typically for permission, if parent is not fully selected, maybe we shouldn't send it?
      // Or pureadmin/backend logic might differ. Let's send checked keys + half checked keys if needed.
      // But my backend RBAC just checks if user has role, and role has menu.
      // If I don't select parent, menu won't show in tree structure?
      // Let's include half checked keys.
      const halfCheckedKeys = treeRef.value!.getHalfCheckedKeys();
      form.value.menu_ids = [...checkedKeys, ...halfCheckedKeys];

      if (form.value.id) {
        await updateRole(form.value.id, form.value);
        message("Role updated", { type: "success" });
      } else {
        await createRole(form.value);
        message("Role created", { type: "success" });
      }
      dialogVisible.value = false;
      fetchData();
    }
  });
};

onMounted(() => {
  fetchData();
  fetchMenus();
});
</script>

<template>
  <div class="main">
    <el-card>
      <template #header>
        <div class="flex justify-between">
          <span>Role Management</span>
          <el-button type="primary" @click="handleAdd">Add Role</el-button>
        </div>
      </template>
      
      <el-table :data="dataList" v-loading="loading" style="width: 100%">
        <el-table-column prop="name" label="Name" />
        <el-table-column prop="code" label="Code" />
        <el-table-column prop="description" label="Description" />
        <el-table-column label="Actions" width="180">
          <template #default="{ row }">
            <el-button link type="primary" @click="handleEdit(row)">Edit</el-button>
            <el-button link type="danger" @click="handleDelete(row)">Delete</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog v-model="dialogVisible" :title="dialogTitle">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="100px">
        <el-form-item label="Name" prop="name">
          <el-input v-model="form.name" />
        </el-form-item>
        <el-form-item label="Code" prop="code">
          <el-input v-model="form.code" :disabled="!!form.id" />
        </el-form-item>
        <el-form-item label="Description" prop="description">
          <el-input v-model="form.description" type="textarea" />
        </el-form-item>
        <el-form-item label="Permissions">
            <el-tree
                ref="treeRef"
                :data="menuList"
                show-checkbox
                node-key="id"
                :props="{ label: 'title', children: 'children' }"
            />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">Cancel</el-button>
        <el-button type="primary" @click="handleSubmit">Confirm</el-button>
      </template>
    </el-dialog>
  </div>
</template>
