<script setup lang="ts">
import { ref, onMounted } from "vue";
import { getLogList, createLog, exportLogs, getExportStatus } from "@/api/log";
import { message } from "@/utils/message";

defineOptions({
  name: "WorkLog"
});

const loading = ref(true);
const dataList = ref([]);
const total = ref(0);
const page = ref(1);
const limit = ref(10);
const dialogVisible = ref(false);
const formRef = ref();

const form = ref({
  content: "",
  completion_status: "Completed",
  issues: "",
  tomorrow_plan: "",
  rating: 100
});

const rules = {
  content: [{ required: true, message: "Content is required", trigger: "blur" }]
};

const fetchData = async () => {
  loading.value = true;
  try {
    const res = await getLogList({ page: page.value, per_page: limit.value });
    dataList.value = res.data.items;
    total.value = res.data.total;
  } finally {
    loading.value = false;
  }
};

const handleAdd = () => {
  form.value = {
    content: "",
    completion_status: "Completed",
    issues: "",
    tomorrow_plan: "",
    rating: 100
  };
  dialogVisible.value = true;
};

const handleSubmit = async () => {
  await formRef.value.validate(async (valid) => {
    if (valid) {
      await createLog(form.value);
      message("Log created", { type: "success" });
      dialogVisible.value = false;
      fetchData();
    }
  });
};

const handleExport = async () => {
    try {
        const res = await exportLogs();
        const taskId = res.data.task_id;
        message("Export started, please wait...", { type: "info" });
        
        // Poll status
        const poll = setInterval(async () => {
            const statusRes = await getExportStatus(taskId);
            const state = statusRes.data.state;
            if (state === 'SUCCESS') {
                clearInterval(poll);
                const downloadUrl = statusRes.data.result;
                // Trigger download
                // VITE_PUBLIC_PATH defaults to /
                const publicPath = import.meta.env.VITE_PUBLIC_PATH.endsWith('/') 
                    ? import.meta.env.VITE_PUBLIC_PATH 
                    : import.meta.env.VITE_PUBLIC_PATH + '/';
                // downloadUrl starts with /static/...
                window.open(publicPath + downloadUrl.substring(1), '_blank');
                message("Export finished", { type: "success" });
            } else if (state === 'FAILURE') {
                clearInterval(poll);
                message("Export failed", { type: "error" });
            }
        }, 2000);
    } catch (e) {
        console.error(e);
    }
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
          <span>Work Logs</span>
          <div>
            <el-button type="success" @click="handleExport">Export Excel</el-button>
            <el-button type="primary" @click="handleAdd">Add Log</el-button>
          </div>
        </div>
      </template>
      
      <el-table :data="dataList" v-loading="loading" style="width: 100%">
        <el-table-column prop="date" label="Date" width="120" />
        <el-table-column prop="user_name" label="User" width="120" />
        <el-table-column prop="content" label="Content" show-overflow-tooltip />
        <el-table-column prop="completion_status" label="Status" width="100" />
        <el-table-column prop="issues" label="Issues" show-overflow-tooltip />
        <el-table-column prop="tomorrow_plan" label="Tomorrow Plan" show-overflow-tooltip />
        <el-table-column prop="rating" label="Rating" width="80" />
        <el-table-column prop="created_at" label="Created At" width="180" />
      </el-table>
      
      <div class="flex justify-end mt-4">
        <el-pagination
          v-model:current-page="page"
          v-model:page-size="limit"
          :total="total"
          layout="total, prev, pager, next"
          @current-change="fetchData"
        />
      </div>
    </el-card>

    <el-dialog v-model="dialogVisible" title="Add Work Log">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="120px">
        <el-form-item label="Content" prop="content">
          <el-input v-model="form.content" type="textarea" :rows="3" />
        </el-form-item>
        <el-form-item label="Status" prop="completion_status">
            <el-select v-model="form.completion_status">
                <el-option label="Completed" value="Completed" />
                <el-option label="In Progress" value="In Progress" />
                <el-option label="Blocked" value="Blocked" />
            </el-select>
        </el-form-item>
        <el-form-item label="Issues" prop="issues">
          <el-input v-model="form.issues" type="textarea" />
        </el-form-item>
        <el-form-item label="Tomorrow Plan" prop="tomorrow_plan">
          <el-input v-model="form.tomorrow_plan" type="textarea" />
        </el-form-item>
        <el-form-item label="Rating" prop="rating">
          <el-slider v-model="form.rating" :min="0" :max="100" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">Cancel</el-button>
        <el-button type="primary" @click="handleSubmit">Confirm</el-button>
      </template>
    </el-dialog>
  </div>
</template>
