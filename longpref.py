class Solution:
    def longestCommonPrefix(self, strs: list[str]) -> str:
        ans = ""
        strs = sorted(strs)
        first = strs[0]
        last = strs[-1]
        for i in range(min(len(first), len(last))):
            if first[i] != last[i]:
                print(first[i])
                return ans
            ans += first[i]


strs = ["flower", "flow", "flight"]
# strs = [""]
# strs = ["a"]
print(Solution().longestCommonPrefix(strs))
