<script setup lang="ts">
import { ref, onMounted } from "vue";
import { getUserList, createUser, updateUser, deleteUser, getRoleList, getPositionList } from "@/api/system";
import { message } from "@/utils/message";
import { ElMessageBox } from "element-plus";

defineOptions({
  name: "UserManagement"
});

const loading = ref(true);
const dataList = ref([]);
const roleList = ref([]);
const positionList = ref([]);
const dialogVisible = ref(false);
const dialogTitle = ref("Add User");
const formRef = ref();

const form = ref({
  id: undefined,
  username: "",
  password: "",
  email: "",
  phone: "",
  position_id: undefined,
  role_ids: [],
  is_active: true
});

const rules = {
  username: [{ required: true, message: "Username is required", trigger: "blur" }],
  password: [{ required: false, message: "Password is required", trigger: "blur" }], // Required only for create
  email: [{ required: true, message: "Email is required", trigger: "blur" }]
};

const fetchData = async () => {
  loading.value = true;
  try {
    const res = await getUserList();
    dataList.value = res.data;
  } finally {
    loading.value = false;
  }
};

const fetchOptions = async () => {
    const roles = await getRoleList();
    roleList.value = roles.data;
    const positions = await getPositionList();
    positionList.value = positions.data;
};

const handleAdd = () => {
  dialogTitle.value = "Add User";
  form.value = {
    id: undefined,
    username: "",
    password: "",
    email: "",
    phone: "",
    position_id: undefined,
    role_ids: [],
    is_active: true
  };
  rules.password[0].required = true;
  dialogVisible.value = true;
};

const handleEdit = (row) => {
  dialogTitle.value = "Edit User";
  form.value = {
    id: row.id,
    username: row.username,
    password: "", // Don't fill password
    email: row.email,
    phone: row.phone,
    position_id: row.position?.id,
    role_ids: row.roles.map(r => r.id),
    is_active: row.is_active
  };
  rules.password[0].required = false;
  dialogVisible.value = true;
};

const handleDelete = (row) => {
  ElMessageBox.confirm(`Are you sure to delete user ${row.username}?`, "Warning", {
    type: "warning"
  }).then(async () => {
    await deleteUser(row.id);
    message("User deleted", { type: "success" });
    fetchData();
  });
};

const handleSubmit = async () => {
  await formRef.value.validate(async (valid) => {
    if (valid) {
      if (form.value.id) {
        await updateUser(form.value.id, form.value);
        message("User updated", { type: "success" });
      } else {
        await createUser(form.value);
        message("User created", { type: "success" });
      }
      dialogVisible.value = false;
      fetchData();
    }
  });
};

onMounted(() => {
  fetchData();
  fetchOptions();
});
</script>

<template>
  <div class="main">
    <el-card>
      <template #header>
        <div class="flex justify-between">
          <span>User Management</span>
          <el-button type="primary" @click="handleAdd">Add User</el-button>
        </div>
      </template>
      
      <el-table :data="dataList" v-loading="loading" style="width: 100%">
        <el-table-column prop="username" label="Username" />
        <el-table-column prop="email" label="Email" />
        <el-table-column prop="phone" label="Phone" />
        <el-table-column label="Position">
            <template #default="{ row }">
                {{ row.position?.name }}
            </template>
        </el-table-column>
        <el-table-column label="Roles">
            <template #default="{ row }">
                <el-tag v-for="role in row.roles" :key="role.id" size="small" class="mr-1">{{ role.name }}</el-tag>
            </template>
        </el-table-column>
        <el-table-column label="Status">
            <template #default="{ row }">
                <el-tag :type="row.is_active ? 'success' : 'danger'">{{ row.is_active ? 'Active' : 'Disabled' }}</el-tag>
            </template>
        </el-table-column>
        <el-table-column label="Actions" width="180">
          <template #default="{ row }">
            <el-button link type="primary" @click="handleEdit(row)" v-track:EditUser="`编辑用户 ${row.username}`">Edit</el-button>
            <el-button link type="danger" @click="handleDelete(row)" v-track:DeleteUser="`删除用户 ${row.username}`">Delete</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog v-model="dialogVisible" :title="dialogTitle">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="100px">
        <el-form-item label="Username" prop="username">
          <el-input v-model="form.username" :disabled="!!form.id" />
        </el-form-item>
        <el-form-item label="Password" prop="password">
          <el-input v-model="form.password" type="password" placeholder="Leave blank to keep unchanged if editing" />
        </el-form-item>
        <el-form-item label="Email" prop="email">
          <el-input v-model="form.email" />
        </el-form-item>
        <el-form-item label="Phone" prop="phone">
          <el-input v-model="form.phone" />
        </el-form-item>
        <el-form-item label="Position" prop="position_id">
            <el-select v-model="form.position_id" placeholder="Select Position">
                <el-option v-for="item in positionList" :key="item.id" :label="item.name" :value="item.id" />
            </el-select>
        </el-form-item>
        <el-form-item label="Roles" prop="role_ids">
            <el-select v-model="form.role_ids" multiple placeholder="Select Roles">
                <el-option v-for="item in roleList" :key="item.id" :label="item.name" :value="item.id" />
            </el-select>
        </el-form-item>
        <el-form-item label="Status" prop="is_active">
            <el-switch v-model="form.is_active" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">Cancel</el-button>
        <el-button type="primary" @click="handleSubmit" v-track:SaveUser="form.id ? '保存用户更新' : '创建新用户'">Confirm</el-button>
      </template>
    </el-dialog>
  </div>
</template>
