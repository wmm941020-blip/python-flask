import { type Directive } from "vue";
import { createLog } from "@/api/log";
import dayjs from "dayjs";

/**
 * 操作日志指令
 * 用法: v-track:CreateUser="{ content: '创建用户', issues: 'xxx' }"
 * 或者简单用法: v-track="'点击了按钮'"
 */
export const track: Directive = {
  mounted(el, binding) {
    el.addEventListener("click", () => {
      const value = binding.value;
      let logData = {
        content: "",
        completion_status: "Completed", // 默认状态
        issues: "",
        tomorrow_plan: "",
        rating: 100,
        date: dayjs().format("YYYY-MM-DD")
      };

      if (typeof value === "string") {
        logData.content = value;
      } else if (typeof value === "object") {
        logData = { ...logData, ...value };
      }

      // 如果有修饰符（arg），可以作为操作类型前缀
      if (binding.arg) {
        logData.content = `[${binding.arg}] ${logData.content}`;
      }

      // 调用接口
      createLog(logData).catch(err => {
        console.error("Auto log failed:", err);
      });
    });
  }
};
