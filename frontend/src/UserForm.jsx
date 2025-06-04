import React, { useState } from "react";

export default function UserForm({ onSubmit }) {
  const [formData, setFormData] = useState({
    chinese_name: '',
    english_name: '',
    gender: '',
    degree: '',
    school_type: '',
    college_type: '',
    school_name: '',
    department: '',
    graduation_year: '',
    has_internship: false,
    joined_bootcamp: false,
    internship_count: 0,
    linkedin_url: '',
  });


  const handleChange = (e) => {
  const { name, value, type, checked } = e.target;

  setFormData((prev) => {
    // 強制將這兩個欄位轉成整數
    if (name === "graduation_year" || name === "internship_count") {
      return {
        ...prev,
        [name]: value === "" ? "" : parseInt(value, 10),
      };
    }

    return {
      ...prev,
      [name]: type === "checkbox" ? checked : value,
    };
  });
};

  const handleSubmit = async (e) => {
  e.preventDefault();

  console.log("送出資料：", JSON.stringify(formData, null, 2));
  console.log("🎓 graduation_year 型別：", typeof formData.graduation_year, formData.graduation_year);

  try {
    const response = await fetch('http://localhost:8001/users', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(formData),
    });

    if (!response.ok) {
      throw new Error('Failed to submit');
    }

    const result = await response.json();
    console.log('✅ Success:', result);
    alert('提交成功！');

  } catch (error) {
    console.error('❌ Error:', error);
    alert('提交失敗');
  }
};

  return (
    <form onSubmit={handleSubmit} className="space-y-4 text-sm">

      <h2 className="text-xl font-bold mb-2">基本資料</h2>

      <input name="chinese_name" value={formData.chinese_name} onChange={handleChange} placeholder="Chinese Name" className="input border px-2 py-1 rounded w-full" />
      <input name="english_name" value={formData.english_name} onChange={handleChange} placeholder="English Name" className="input border px-2 py-1 rounded w-full" />
      <input name="gender" value={formData.gender} onChange={handleChange} placeholder="Gender" className="input border px-2 py-1 rounded w-full" />
      <input name="degree" value={formData.degree} onChange={handleChange} placeholder="Degree" className="input border px-2 py-1 rounded w-full" />
      <input name="school_type" value={formData.school_type} onChange={handleChange} placeholder="School Type (公立 / 私立)" className="input border px-2 py-1 rounded w-full" />
      <input name="college_type" value={formData.college_type} onChange={handleChange} placeholder="College Type (普通大學 / 科技大學)" className="input border px-2 py-1 rounded w-full" />
      <input name="school_name" value={formData.school_name} onChange={handleChange} placeholder="School Name" className="input border px-2 py-1 rounded w-full" />
      <input name="department" value={formData.department} onChange={handleChange} placeholder="Department" className="input border px-2 py-1 rounded w-full" />
      <input name="graduation_year" value={formData.graduation_year} onChange={handleChange} placeholder="Graduation Year" type="number" className="input border px-2 py-1 rounded w-full" />

      <input name="linkedin_url" value={formData.linkedin_url} onChange={handleChange} placeholder="LinkedIn URL" className="input border px-2 py-1 rounded w-full" />

      <div className="flex items-center space-x-2">
        <input type="checkbox" name="has_internship" checked={formData.has_internship} onChange={handleChange} />
        <label htmlFor="has_internship">Has Internship</label>
      </div>

      <div className="flex items-center space-x-2">
        <input type="checkbox" name="joined_bootcamp" checked={formData.joined_bootcamp} onChange={handleChange} />
        <label htmlFor="joined_bootcamp">Joined Bootcamp</label>
      </div>

      <input name="internship_count" value={formData.internship_count} onChange={handleChange} placeholder="Internship Count" type="number" className="input border px-2 py-1 rounded w-full" />

      <button type="submit" className="bg-cyan-600 text-white px-4 py-2 rounded hover:bg-cyan-700">
        🚀 提交表單
      </button>
    </form>

  );
}
