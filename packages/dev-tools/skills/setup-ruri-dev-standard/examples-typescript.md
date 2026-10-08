#### 示例 (TypeScript / Bun):

```typescript
/**
 * 结构化解析 Table.pak 解压出的二进制 Header，确定 CSV 文件的偏移量指针。
 *
 * 传入 Pak 缓冲 Buffer，返回解析后的段表元数据数组。
 */
export interface PakHeaderSegment {
  offset: number;
  length: number;
}

```
